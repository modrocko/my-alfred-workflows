import os
import json
import sys

query = sys.argv[1].lower() if len(sys.argv) > 1 else ""

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    emails = json.load(f)

# Count how many emails under each tag
tag_counts = {}
for tag_group in emails:
    tag = tag_group.get("tag", "")
    email_list = tag_group.get("emails", [])
    if tag:
        tag_counts[tag] = len(email_list)

# Filter & sort tags
filtered_tags = sorted(tag for tag in tag_counts if query in tag.lower()) if query else sorted(tag_counts)

# Build Alfred results
items = []
for tag in filtered_tags:
    count = tag_counts[tag]
    items.append({
        "title": tag,
        "subtitle": f"{count} email{'s' if count != 1 else ''} • ↵ view • ⌘ remove • ⌥ rename • ⌃ tag • ⇧ view all",
        "arg": tag,
        "mods": {
            "cmd": {
                "arg": tag,
                "subtitle": f"Remove tag: {tag}"
            },
            "alt": {
                "arg": tag,
                "subtitle": f"Rename tag: {tag}",
                "variables": {
                    "old_tag": tag
                }
            },
            "ctrl": {
                "arg": tag,
                "subtitle": f"Tag mail with: {tag}"
            },
            "shift": {
                "arg": tag,
                "subtitle": f"Open all emails with: {tag}"
            }
        }
    })


if not items:
    items = [{
        "title": "No tagged bookmarks found",
        "valid": False
    }]

print(json.dumps({"items": items}))
