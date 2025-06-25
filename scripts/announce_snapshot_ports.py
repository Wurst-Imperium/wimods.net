import util
from argparse import ArgumentParser
from pathlib import Path

current_snapshot_discussion = 1190


def get_link(mod: str, branch: str) -> str:
	props = util.read_gradle_properties(mod, branch)
	version = props["mod_version"].removeprefix("v")
	version = version[: version.index("-MC")]

	if mod == "wurst7":
		return f"https://www.wurstclient.net/updates/wurst-{version.replace('.', '-')}?mc={branch}"
	else:
		return f"https://www.wimods.net/{mod}/{mod}-{version.replace('.', '-')}?mc={branch}"


def main(snapshot: str, included_mods: list[str], dry_run: bool):
	config = util.read_toml_file(Path("config.toml"))
	possible_mod_names = config["Params"]["modnames"]
	possible_mod_names["wurst7"] = "Wurst"
	mod_names = [possible_mod_names[mod] for mod in included_mods]

	if len(included_mods) == 1:
		mods_string = mod_names[0]
	else:
		mods_string = f"{', '.join(mod_names[:-1])} and {mod_names[-1]}"
	content = f"{mods_string} {'has' if len(included_mods) == 1 else 'have'} been updated to support Minecraft {snapshot}!\n\n"

	for mod in included_mods:
		content += f"{possible_mod_names[mod]}: <{get_link(mod, snapshot)}>\n"
	content += "\nEnjoy! 🤖"

	util.upload_post(current_snapshot_discussion, content, dry_run=dry_run)


if __name__ == "__main__":
	parser = ArgumentParser(description="Announces a new mod update on WurstForum")
	parser.add_argument("snapshot", help="Snapshot branch name (e.g. '25w03a')")
	parser.add_argument("mods", nargs="+", help="Mods to include in the announcement")
	parser.add_argument(
		"--dry-run", action="store_true", help="Don't actually upload the announcement"
	)
	args = parser.parse_args()
	main(args.snapshot, args.mods, args.dry_run)
