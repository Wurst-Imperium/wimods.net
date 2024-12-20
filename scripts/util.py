import json
import os
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

yaml = YAML()
yaml.preserve_quotes = True


@dataclass
class JekyllPost:
	front_matter: CommentedMap
	content: str
	path: Path


def read_post(path: Path) -> JekyllPost:
	"""Read front matter and content from a Jekyll/Hugo post."""
	content = path.read_text(encoding="utf-8")
	parts = content.split("---", 2)
	if len(parts) < 3:
		raise ValueError(f"Invalid front matter format in {path}")

	return JekyllPost(yaml.load(parts[1]), parts[2].strip(), path)


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


def find_mod_update_post(mod: str, version: str) -> JekyllPost:
	"""Find the mod update post for a specific version."""
	posts_folder = Path("content") / mod
	version_slug = version.replace(".", "-")
	for post_path in posts_folder.rglob(f"*-{version_slug}.md"):
		if not post_path.is_file():
			continue

		post = read_post(post_path)
		if post.front_matter.get("modversion") == version:
			return post

	raise ValueError(f"Could not find post for mod {mod} version {version}")


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


def set_github_output(key: str, value: str):
	"""Set a key-value pair in the GitHub Actions output."""
	if "GITHUB_OUTPUT" not in os.environ:
		print(f"Not running on GHA, would have set output: {key}={value}")
		return
	with open(os.environ["GITHUB_OUTPUT"], "a") as env:
		print(f"{key}={value}", file=env)
