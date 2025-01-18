import json
import os
import requests
import tomli
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from typing import Iterator

yaml = YAML()
yaml.preserve_quotes = True


@dataclass
class HugoPost:
	front_matter: CommentedMap
	content: str
	path: Path

	def get_update_url(self) -> str:
		mod = self.front_matter["mod"]
		version = self.front_matter["modversion"]
		return f"https://www.wimods.net/{mod}/{mod}-{version.replace('.', '-')}/"

	def get_date(self) -> datetime:
		return datetime.fromisoformat(str(self.front_matter["date"]))

	def get_mod_version(self) -> str:
		return self.front_matter["modversion"]

	def get_mc_versions(self, modloader: str) -> list[str]:
		if modloader == "fabric":
			return [
				v
				for v in self.front_matter.get("mcversions", [])
				if v not in self.front_matter.get("nofabric", [])
			]
		if modloader == "neoforge":
			return self.front_matter.get("neoforge", [])
		raise ValueError(f"Invalid modloader: {modloader}")


@dataclass
class WurstForumDiscussion:
	title: str
	tags: list[int]
	content: str


def read_post(path: Path) -> HugoPost:
	"""Read front matter and content from a Jekyll/Hugo post."""
	content = path.read_text(encoding="utf-8")
	parts = content.split("---", 2)
	if len(parts) < 3:
		raise ValueError(f"Invalid front matter format in {path}")

	return HugoPost(yaml.load(parts[1]), parts[2].strip(), path)


def write_front_matter(path: Path, front_matter: CommentedMap):
	"""Write YAML front matter to a Jekyll/Hugo post while preserving content."""
	content = path.read_text(encoding="utf-8")
	parts = content.split("---", 2)
	if len(parts) < 3:
		raise ValueError(f"Invalid front matter format in {path}")

	output = StringIO()
	yaml.dump(front_matter, output)
	new_content = f"---\n{output.getvalue()}---{parts[2]}"
	path.write_text(new_content, encoding="utf-8", newline="\n")


def get_mod_update_posts(mod: str) -> Iterator[HugoPost]:
	"""Get all update post paths for the given mod."""
	posts_folder = Path("content") / mod
	for post_path in posts_folder.rglob("*.md"):
		if post_path.is_file() and post_path.name.lower().startswith(mod):
			yield read_post(post_path)


def find_mod_update_post(mod: str, version: str) -> HugoPost:
	"""Find and read the mod update post for a specific version."""
	for post in get_mod_update_posts(mod):
		if post.get_mod_version() == version:
			return post

	raise ValueError(f"Could not find post for mod {mod} version {version}")


def parse_changelog(content: str) -> str:
	"""Parse the changelog from the content of a mod update post."""
	changelog_lines = []
	for line in content[content.find("## Changelog") :].splitlines():
		stripped = line.strip()
		if not stripped or stripped.startswith("-") or stripped.startswith("## Changelog"):
			changelog_lines.append(line)
			continue
		break
	return "\n".join(changelog_lines).strip()


def upload_discussion(discussion: WurstForumDiscussion, dry_run: bool = False) -> int:
	"""Upload a new discussion to WurstForum and return its ID."""
	url = "https://wurstforum.net/api/discussions"
	headers = {"Authorization": f"Token {os.getenv('WURSTFORUM_TOKEN')}"}
	data = {
		"data": {
			"type": "discussions",
			"attributes": {
				"title": discussion.title,
				"content": discussion.content,
			},
			"relationships": {
				"tags": {
					"data": [{"type": "tags", "id": tag_id} for tag_id in discussion.tags],
				},
			},
		},
	}

	print(f"Request data: {json.dumps(data, indent=2)}")
	if dry_run:
		return 123

	response = requests.post(url, headers=headers, json=data)
	if not response.ok:
		raise requests.HTTPError(f"Request failed (code {response.status_code}): {response.text}")
	discussion_id = response.json().get("data", {}).get("id")
	if not discussion_id:
		raise ValueError(f"No discussion ID in response: {response.text}")
	return discussion_id


def read_yaml_file(path: Path) -> CommentedMap | CommentedSeq:
	"""Read a YAML data file."""
	return yaml.load(path.read_text(encoding="utf-8"))


def write_yaml_file(path: Path, data: CommentedMap | CommentedSeq):
	"""Write a YAML data file."""
	output = StringIO()
	yaml.dump(data, output)
	path.write_text(output.getvalue(), encoding="utf-8", newline="\n")


def read_json_file(path: Path) -> dict:
	"""Read a JSON data file."""
	return json.loads(path.read_text(encoding="utf-8"))


def write_json_file(path: Path, data: dict):
	"""Write a JSON data file."""
	path.write_text(json.dumps(data, indent=2), encoding="utf-8", newline="\n")


def read_toml_file(path: Path) -> dict:
	"""Read a TOML data file."""
	return tomli.loads(path.read_text(encoding="utf-8"))


def set_github_output(key: str, value: str):
	"""Set a key-value pair in the GitHub Actions output."""
	if "GITHUB_OUTPUT" not in os.environ:
		print(f"Not running on GHA, would have set output: {key}={value}")
		return
	with open(os.environ["GITHUB_OUTPUT"], "a") as env:
		print(f"{key}={value}", file=env)
