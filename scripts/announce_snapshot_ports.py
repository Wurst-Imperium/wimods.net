import util
from argparse import ArgumentParser
from pathlib import Path


def get_current_snapshot_discussion() -> int:
	cycle = util.read_json_file(Path("data/current_snapshot_cycle.json"))
	return cycle["wurstforum_discussion"]


def get_link(mod: str, mc_version: str, branch: str) -> str:
	props = util.read_gradle_properties(mod, branch)
	version = props["mod_version"].removeprefix("v")
	version = version[: version.index("-MC")]

	if mod == "wurst7":
		return (
			f"https://www.wurstclient.net/updates/wurst-{version.replace('.', '-')}?mc={mc_version}"
		)
	else:
		return f"https://www.wimods.net/{mod}/{mod}-{version.replace('.', '-')}?mc={mc_version}"


def main(mc_version: str, branch: str, included_mods: list[str], dry_run: bool):
	config = util.read_toml_file(Path("config.toml"))
	possible_mod_names = config["Params"]["modnames"]
	possible_mod_names["wurst7"] = "Wurst"
	mod_names = [possible_mod_names[mod] for mod in included_mods]

	if len(included_mods) == 1:
		mods_string = mod_names[0]
	else:
		mods_string = f"{', '.join(mod_names[:-1])} and {mod_names[-1]}"
	content = f"{mods_string} {'has' if len(included_mods) == 1 else 'have'} been updated to support Minecraft {mc_version}!\n\n"

	for mod in included_mods:
		content += f"{possible_mod_names[mod]}: <{get_link(mod, mc_version, branch)}>\n"
	content += "\nEnjoy! 🤖"

	discussion_id = get_current_snapshot_discussion()
	util.upload_post(discussion_id, content, dry_run=dry_run)


if __name__ == "__main__":
	parser = ArgumentParser(description="Announces a new mod update on WurstForum")
	parser.add_argument("mc_version", help="Minecraft version (e.g. '25w03a')")
	parser.add_argument("branch", help="Branch name (e.g. '1.21.5')")
	parser.add_argument("mods", nargs="+", help="Mods to include in the announcement")
	parser.add_argument(
		"--dry-run", action="store_true", help="Don't actually upload the announcement"
	)
	args = parser.parse_args()
	main(args.mc_version, args.branch, args.mods, args.dry_run)
