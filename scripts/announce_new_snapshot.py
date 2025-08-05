import util
from argparse import ArgumentParser


def get_link(mc_version: str) -> str:
	"""Guess the Minecraft.net blog post URL for the given version."""
	prefix = "https://www.minecraft.net/en-us/article"
	if mc_version.lower().startswith("1."):
		if "-pre" in mc_version:
			# e.g. 1.21.6-pre1 -> minecraft-1-21-6-pre-release-1
			base, pre = mc_version.split("-pre")
			base = base.replace(".", "-")
			return f"{prefix}/minecraft-{base}-pre-release-{pre}"
		elif "-rc" in mc_version:
			# e.g. 1.21.6-rc1 -> minecraft-1-21-6-release-candidate-1
			base, rc = mc_version.split("-rc")
			base = base.replace(".", "-")
			return f"{prefix}/minecraft-{base}-release-candidate-{rc}"
		else:
			# e.g. 1.21.8 -> minecraft-java-edition-1-21-8
			base = mc_version.replace(".", "-")
			return f"{prefix}/minecraft-java-edition-{base}"
	else:
		# e.g. 25w21a -> minecraft-snapshot-25w21a
		return f"{prefix}/minecraft-snapshot-{mc_version.lower()}"


def main(mc_version: str, dry_run: bool):
	content = f"A new Minecraft version has been released: [{mc_version}]({get_link(mc_version)})"
	discussion_id = util.get_current_snapshot_discussion()
	util.upload_post(discussion_id, content, dry_run=dry_run)


if __name__ == "__main__":
	parser = ArgumentParser(description="Announces a new Minecraft snapshot on WurstForum")
	parser.add_argument("mc_version", help="Minecraft version (e.g. '25w03a')")
	parser.add_argument(
		"--dry-run", action="store_true", help="Don't actually upload the announcement"
	)
	args = parser.parse_args()
	main(args.mc_version, args.dry_run)
