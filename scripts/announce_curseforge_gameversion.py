import util
from argparse import ArgumentParser


def main(version: str, type_name: str, dry_run: bool):
	content = f"CurseForge has added a new game version: {version} (type: {type_name})"
	discussion_id = util.get_current_snapshot_discussion()
	util.upload_post(discussion_id, content, dry_run=dry_run)


if __name__ == "__main__":
	parser = ArgumentParser(description="Announces a new CurseForge game version on WurstForum")
	parser.add_argument("version", help="CurseForge game version (e.g. '1.21.11-snapshot')")
	parser.add_argument("type_name", help="Version type name (e.g. 'Minecraft 1.21')")
	parser.add_argument(
		"--dry-run", action="store_true", help="Don't actually upload the announcement"
	)
	args = parser.parse_args()
	main(args.version, args.type_name, args.dry_run)
