import util
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from util import HugoPost, WurstForumDiscussion


@dataclass
class ModTarget:
	mc_version: str
	modloader: str

	@classmethod
	def from_branch(cls, mod: str, branch: str) -> "ModTarget":
		"""Extract MC version and modloader from gradle.properties in the given branch."""
		props = util.read_gradle_properties(mod, branch)

		mc_version = props.get("minecraft_version")
		if not mc_version:
			raise ValueError(f"Could not find Minecraft version in {mod}@{branch}")

		if "fabric_api_version" in props:
			modloader = "fabric"
		elif "neo_version" in props:
			modloader = "neoforge"
		else:
			raise ValueError(f"Could not determine modloader in {mod}@{branch}")

		return cls(mc_version, modloader)

	def __str__(self) -> str:
		modloader_name = "Fabric" if self.modloader == "fabric" else "NeoForge"
		return f"{self.mc_version} ({modloader_name})"


def find_update_before(mod: str, before_date: datetime, target: ModTarget) -> HugoPost | None:
	"""Find the newest mod update before before_date that was available for target."""
	latest_post = None
	for post in util.get_mod_update_posts(mod):
		if post.get_date() >= before_date:
			continue
		if target.mc_version in post.get_mc_versions_including_snapshots(target.modloader):
			if latest_post is None or post.get_date() > latest_post.get_date():
				latest_post = post
	return latest_post


def find_updates_between(mod: str, start_date: datetime, end_date: datetime) -> list[HugoPost]:
	"""Find all mod update posts between start_date and end_date, in chronological order."""
	updates = []
	for post in util.get_mod_update_posts(mod):
		post_date = post.get_date()
		if post_date > start_date and post_date <= end_date:
			updates.append(post)
	return sorted(updates, key=lambda p: p.get_date())


def combine_changelogs(
	mod: str,
	mod_name: str,
	target: ModTarget,
	current_update: HugoPost,
	prev_update: HugoPost | None,
) -> str:
	if prev_update is None:
		print(f"No previous update found for {target}")
		return f"This is the first {mod_name} version to support Minecraft {target}!"
	print(f"Previous update for {target}: {prev_update.get_mod_version()}")
	changelogs = []
	update_posts = find_updates_between(mod, prev_update.get_date(), current_update.get_date())
	print(
		f"Updates for {target} between {prev_update.get_mod_version()} and {current_update.get_mod_version()}: "
		f"{[post.get_mod_version() for post in update_posts]}"
	)
	for post in update_posts:
		changelog = util.parse_changelog(post.content)
		update_url = post.get_update_url()
		new_heading = f"### Changes from [{mod_name} {post.get_mod_version()}]({update_url})\n"
		# Filter out posts with multiple "## Changelog" headings
		if changelog.startswith("## Changelog\n") and changelog.count("## Changelog") == 1:
			changelog = changelog[len("## Changelog\n") :]
			changelogs.append(new_heading + changelog)
		else:
			changelogs.append(
				new_heading
				+ "Multiple changelogs found. Don't know which one to show here. See <{update_url}>."
			)
	return "\n\n".join(changelogs)


announcement_template_one_no_changes = """
{mod_name} {mod_version} has been ported to Minecraft {target}.

Download it here: <{update_url}>

This is the first {mod_name} version to support Minecraft {target}!
""".strip()


announcement_template_one = """
{mod_name} {mod_version} has been ported to Minecraft {target}.

Download it here: <{update_url}>

This port makes the following changes accessible to Minecraft {target} players:

{changelogs}

**Note:** Since these changelogs are taken directly from previous {mod_name} updates that did not originally support \
Minecraft {target}, they might sometimes not make sense in this context.
""".strip()


announcement_template_multiple = """
{mod_name} {mod_version} has been ported to several new Minecraft versions: {mod_targets}.

Download it here: <{update_url}>

This port makes the following changes accessible to players of each Minecraft version:

{changelogs}

**Note:** Since these changelogs are taken directly from previous {mod_name} updates that did not originally support \
these Minecraft versions, they might sometimes not make sense in this context.
""".strip()


def main(mod: str, mod_version: str, mod_targets: list[ModTarget], dry_run: bool):
	config = util.read_toml_file(Path("config.toml"))
	mod_name = config["Params"]["modnames"][mod]

	# Title
	formatted_targets = " / ".join(str(target) for target in mod_targets)
	title = f"{mod_name} {mod_version} ported to Minecraft {formatted_targets}"
	if len(title) > 80:
		title = f"{mod_name} {mod_version} ported to new Minecraft versions"

	# Tag IDs - check these at https://wurstforum.net/api/tags
	tags = {
		"Announcements": 3,
		"Other Mods": 27,
	}

	# Content (changelogs)
	current_update = util.find_mod_update_post(mod, mod_version)
	if len(mod_targets) == 1:
		target = mod_targets[0]
		prev_update = find_update_before(mod, current_update.get_date(), target)
		if prev_update is None:
			content = announcement_template_one_no_changes.format(
				mod_name=mod_name,
				mod_version=mod_version,
				target=target,
				update_url=f"{current_update.get_update_url()}?mc={target.mc_version}",
			)
		else:
			content = announcement_template_one.format(
				mod_name=mod_name,
				mod_version=mod_version,
				target=target,
				update_url=f"{current_update.get_update_url()}?mc={target.mc_version}",
				changelogs=combine_changelogs(mod, mod_name, target, current_update, prev_update),
			)
	else:
		changelogs = []
		for target in mod_targets:
			prev_update = find_update_before(mod, current_update.get_date(), target)
			changelogs.append(
				f"## Changes for Minecraft {target} players\n\n"
				+ combine_changelogs(mod, mod_name, target, current_update, prev_update)
			)
		content = announcement_template_multiple.format(
			mod_name=mod_name,
			mod_version=mod_version,
			mod_targets=", ".join(str(target) for target in mod_targets),
			update_url=current_update.get_update_url(),
			changelogs="\n\n".join(changelogs),
		)

	# Upload announcement
	announcement = WurstForumDiscussion(title, list(tags.values()), content)
	util.upload_discussion(announcement, dry_run=dry_run)


if __name__ == "__main__":
	parser = ArgumentParser(description="Announces a new set of mod ports on WurstForum")
	parser.add_argument("mod", help="Mod ID (as it appears in config.toml)")
	parser.add_argument("mod_version", help="Mod version (without v or -MC)")
	parser.add_argument("branches", nargs="+", help="Branch names (e.g. 'master 1.21.3-neoforge')")
	parser.add_argument(
		"--dry-run", action="store_true", help="Don't actually upload the announcement"
	)
	args = parser.parse_args()
	mod_targets = [ModTarget.from_branch(args.mod, branch) for branch in args.branches]
	main(args.mod, args.mod_version, mod_targets, args.dry_run)
