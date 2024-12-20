import argparse
import json
import os
import requests
import util
from dataclasses import dataclass
from pathlib import Path
from util import HugoPost


@dataclass
class WurstForumDiscussion:
	title: str
	tags: list[int]
	content: str


announcement_template = """
@"Everyone"#g7 {mod_name} {mod_version} is now available. Download it here: <{update_url}>

[![{title}]({image_url})]({update_url})

{changelog}
""".strip()


def parse_changelog(content: str) -> str:
	"""Parse the changelog from the content of a Wurst update post."""
	changelog_lines = []
	for line in content[content.find("## Changelog") :].splitlines():
		stripped = line.strip()
		if not stripped or stripped.startswith("-") or stripped.startswith("## Changelog"):
			changelog_lines.append(line)
			continue
		break
	return "\n".join(changelog_lines).strip()


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
		update_url=f"https://www.wimods.net/{mod}/{mod}-{mod_version.replace('.', '-')}/",
		image_url=mod_update.front_matter["image"],
		changelog=parse_changelog(mod_update.content),
	)

	return WurstForumDiscussion(title, list(tags.values()), content)


def upload_discussion(discussion: WurstForumDiscussion) -> int:
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
	response = requests.post(url, headers=headers, json=data)
	if not response.ok:
		raise requests.HTTPError(f"Request failed (code {response.status_code}): {response.text}")
	discussion_id = response.json().get("data", {}).get("id")
	if not discussion_id:
		raise ValueError(f"No discussion ID in response: {response.text}")
	return discussion_id


def main(mod, mod_version):
	hugo_post = util.find_mod_update_post(mod, mod_version)

	announcement = create_announcement(hugo_post)
	print(f"Title: {announcement.title}")
	print(f"Content: {announcement.content}")

	discussion_id = upload_discussion(announcement)
	print(f"https://wurstforum.net/d/{discussion_id}")
	util.set_github_output("discussion_id", discussion_id)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Announces a new mod update on WurstForum")
	parser.add_argument("mod", help="Mod ID (as it appears in config.toml)")
	parser.add_argument("mod_version", help="Mod version (without v or -MC)")
	args = parser.parse_args()
	main(args.mod, args.mod_version)
