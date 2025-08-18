import util
from argparse import ArgumentParser


def main(fapi_version: str, mc_version: str, dry_run: bool):
	content = f"Fabric API for {mc_version} has been released: `{fapi_version}`"
	discussion_id = util.get_current_snapshot_discussion()
	util.upload_post(discussion_id, content, dry_run=dry_run)


if __name__ == "__main__":
	parser = ArgumentParser(description="Announces Fabric API for a snapshot on WurstForum")
	parser.add_argument("fapi_version", help="Fabric API version (e.g. '0.115.0+1.21.5')")
	parser.add_argument("mc_version", help="Minecraft version (e.g. '25w03a')")
	parser.add_argument(
		"--dry-run", action="store_true", help="Don't actually upload the announcement"
	)
	args = parser.parse_args()
	main(args.fapi_version, args.mc_version, args.dry_run)
