import json
import os
import requests
from argparse import ArgumentParser
from io import StringIO
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
manifest = requests.get(manifest_url).json()

version_info = {
	version["id"]: {"type": version["type"], "releaseTime": version["releaseTime"]}
	for version in manifest["versions"]
}


def read_front_matter(path):
	"""Read YAML front matter from a Jekyll/Hugo post."""
	with open(path, "r", encoding="utf-8") as file:
		content = file.read()

	# Split on the first two "---" markers
	parts = content.split("---", 2)
	if len(parts) < 3:
		raise ValueError(f"Invalid front matter format in {path}")

	# Parse the YAML between the markers
	return yaml.load(parts[1])


def write_front_matter(path, front_matter):
	"""Write YAML front matter to a Jekyll/Hugo post while preserving content."""
	with open(path, "r", encoding="utf-8") as file:
		content = file.read()

	# Split the original content
	parts = content.split("---", 2)
	if len(parts) < 3:
		raise ValueError(f"Invalid front matter format in {path}")

	# Create new content with updated front matter
	output = StringIO()
	yaml.dump(front_matter, output)
	new_content = f"---\n{output.getvalue()}---{parts[2]}"

	# Write the updated content
	with open(path, "w", encoding="utf-8") as file:
		file.write(new_content)


def find_mod_update_post(mod, version):
	"""Find the mod update post for a specific version."""
	posts_folder = os.path.join("content", mod)
	for root, _, files in os.walk(posts_folder):
		for file in files:
			version_slug = version.replace(".", "-")
			if version_slug not in file:
				continue

			post_path = os.path.join(root, file)
			front_matter = read_front_matter(post_path)
			if front_matter["modversion"] == version:
				return front_matter, post_path

	raise ValueError(f"Could not find post for mod {mod} version {version}")


def update_mod_post(mod, modloader, mod_version, mc_version):
	"""Add a new Minecraft version to a mod update post."""
	mc_version_type = version_info[mc_version]["type"]
	front_matter, post_path = find_mod_update_post(mod, mod_version)

	if mc_version_type == "snapshot":
		if "snapshots" not in front_matter:
			front_matter["snapshots"] = []
		if mc_version not in front_matter["snapshots"]:
			front_matter["snapshots"].insert(0, mc_version)
			front_matter["snapshots"].sort(
				key=lambda v: version_info[v]["releaseTime"],
				reverse=True,
			)
	elif mc_version not in front_matter["mcversions"]:
		front_matter["mcversions"].insert(0, mc_version)
		front_matter["mcversions"].sort(
			key=lambda v: version_info[v]["releaseTime"],
			reverse=True,
		)

	if modloader == "neoforge":
		if "neoforge" not in front_matter:
			front_matter["neoforge"] = []
		if mc_version not in front_matter["neoforge"]:
			front_matter["neoforge"].insert(0, mc_version)
			front_matter["neoforge"].sort(
				key=lambda v: version_info[v]["releaseTime"],
				reverse=True,
			)

	write_front_matter(post_path, front_matter)


def update_fabric_api_data(mod, mod_version, mc_version, fapi_version):
	"""Add a new entry to the Fabric API data file for a mod."""
	data_file = os.path.join("data", "fabric_api", f"{mod}.json")
	with open(data_file, "r") as f:
		data = json.load(f)

	# Add mod_version -> mc_version -> fabric_api mapping unless it is already there
	if mod_version not in data:
		data[mod_version] = {}
	if mc_version not in data[mod_version]:
		data[mod_version][mc_version] = fapi_version

	# Sort fabric_api by release time and version type
	for mod_version in data:
		data[mod_version] = {
			k: v
			for k, v in sorted(
				data[mod_version].items(),
				key=lambda item: (
					version_info[item[0]]["type"] == "release",
					version_info[item[0]]["releaseTime"],
				),
				reverse=True,
			)
		}

	with open(data_file, "w") as f:
		json.dump(data, f, indent=2)


def update_curseforge_data(mod, modloader, mod_version, mc_version, file_id):
	"""Add a new entry to the CurseForge data file for a mod."""
	data_file = os.path.join("data", "curseforge", f"{mod}", f"{modloader}.json")
	with open(data_file, "r") as f:
		data = json.load(f)

	# Add mod_version -> mc_version mapping unless it is already there
	if mod_version not in data:
		data[mod_version] = {}
	if mc_version not in data[mod_version]:
		data[mod_version][mc_version] = int(file_id)

	# Sort curseforge IDs by release time and version type
	for mod_version in data:
		data[mod_version] = {
			k: v
			for k, v in sorted(
				data[mod_version].items(),
				key=lambda item: (
					version_info[item[0]]["type"] == "release",
					version_info[item[0]]["releaseTime"],
				),
				reverse=True,
			)
		}

	with open(data_file, "w") as f:
		json.dump(data, f, indent=2)


def add_download_category(mod, new_mcversion, old_mcversion):
	"""Add a new download category when a mod is ported to a new Minecraft version."""
	old_page_path = os.path.join(
		"content", mod, f"minecraft-{old_mcversion.replace('.', '-')}.html"
	)
	new_page_path = os.path.join(
		"content", mod, f"minecraft-{new_mcversion.replace('.', '-')}.html"
	)

	front_matter = read_front_matter(old_page_path)
	title = front_matter["title"]
	description = front_matter["description"]

	front_matter["title"] = title.replace(old_mcversion, new_mcversion)
	front_matter["description"] = description.replace(old_mcversion, new_mcversion)
	front_matter["mcversion"] = new_mcversion

	with open(new_page_path, "w", encoding="utf-8") as f:
		f.writelines(["---", "---", "\n"])
	write_front_matter(new_page_path, front_matter)


def main(mod, modloader, mod_version, mc_version, fapi_version, file_id):
	# Update post
	update_mod_post(mod, modloader, mod_version, mc_version)

	# Update data files
	update_curseforge_data(mod, modloader, mod_version, mc_version, file_id)
	if modloader == "fabric":
		update_fabric_api_data(mod, mod_version, mc_version, fapi_version)

	# Add download category
	mc_version_type = version_info[mc_version]["type"]
	if mc_version_type == "release" and mc_version == manifest["latest"]["release"]:
		old_latest = sorted(
			[v for v in manifest["versions"] if v["type"] == "release"],
			key=lambda v: v["releaseTime"],
			reverse=True,
		)[1]["id"]
		add_download_category(mod, mc_version, old_latest)


if __name__ == "__main__":
	parser = ArgumentParser(
		description="Adds the necessary Hugo metadata when an existing mod update is ported to a new Minecraft version"
	)
	parser.add_argument("mod", help="Mod ID (as it appears in config.toml)")
	parser.add_argument("modloader", help="Mod loader (fabric or neoforge)")
	parser.add_argument("mod_version", help="Mod version (without v or -MC)")
	parser.add_argument("mc_version", help="Minecraft version")
	parser.add_argument("--fapi_version", help="Fabric API version")
	parser.add_argument("file_id", help="CurseForge file ID")

	args = parser.parse_args()
	if args.modloader == "fabric" and not args.fapi_version:
		parser.error("--fapi-version is required for Fabric builds")

	main(
		args.mod, args.modloader, args.mod_version, args.mc_version, args.fapi_version, args.file_id
	)
