import util
from argparse import ArgumentParser
from pathlib import Path
from util import HugoPost, WurstForumDiscussion

announcement_template = """
@"Everyone"#g7 {mod_name} {mod_version} is now available. Download it here: <{update_url}>

[![{title}]({image_url})]({update_url})

{changelog}
""".strip()


def create_announcement(mod_update: HugoPost) -> WurstForumDiscussion:
	"""Create an announcement from a mod update post."""
	# Title
	title = mod_update.front_matter["title"]

	# Tag IDs - check these at https://wurstforum.net/api/tags
	tags = {
		"Announcements": 3,
		"Other Mods": 27,
	}

	# Content
	mod = mod_update.front_matter["mod"]
	config = util.read_toml_file(Path("config.toml"))
	mod_name = config["Params"]["modnames"][mod]
	mod_version = mod_update.front_matter["modversion"]
	content = announcement_template.format(
		title=title,
		mod_name=mod_name,
		mod_version=mod_version,
		update_url=mod_update.get_update_url(),
		image_url=mod_update.front_matter["image"],
		changelog=util.parse_changelog(mod_update.content),
	)

	return WurstForumDiscussion(title, list(tags.values()), content)


def main(mod, mod_version, dry_run):
	hugo_post = util.find_mod_update_post(mod, mod_version)
	announcement = create_announcement(hugo_post)
	util.upload_discussion(announcement, dry_run=dry_run)


if __name__ == "__main__":
	parser = ArgumentParser(description="Announces a new mod update on WurstForum")
	parser.add_argument("mod", help="Mod ID (as it appears in config.toml)")
	parser.add_argument("mod_version", help="Mod version (without v or -MC)")
	parser.add_argument(
		"--dry-run", action="store_true", help="Don't actually upload the announcement"
	)
	args = parser.parse_args()
	main(args.mod, args.mod_version, args.dry_run)
