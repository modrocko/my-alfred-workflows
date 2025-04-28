import os
import sys
import json

query = sys.argv[1].replace("!", "❗").lower() if len(sys.argv) > 1 else ""

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")
default_tags_path = os.path.join(workflow_dir, "default-tags.json")

# Load default tags
default_tags = []
if os.path.exists(default_tags_path):
    with open(default_tags_path, "r") as f:
        default_tags = json.load(f)

# Load assigned tags from bookmarks
assigned_tags = set()
if os.path.exists(db_path):
    with open(db_path, "r") as f:
        bookmarks = json.load(f)
        for bm in bookmarks:
            tag = bm.get("tag", "")
            if tag:
                assigned_tags.add(tag)

# Combine tags
all_tags = set(default_tags) | assigned_tags

# Filter
filtered = sorted(t for t in all_tags if query in t.lower())

# Always include typed query if it's not already a tag
if query and query not in [t.lower() for t in all_tags]:
    filtered.insert(0, query)

# Build Alfred items
items = [{
    "title": tag,
    "subtitle": "↵ tag tab  •  ⌘ tag tabs in front window •  ⌃ tag tabs across windows",
    "arg": tag,
    "mods": {
        "cmd": {
            "arg": tag,
            "subtitle": "⌘↵ to tag all tabs in front window",
            "variables": {
                "tag_all_tabs": "1"
            }
        },
        "ctrl": {
            "arg": tag,
            "subtitle": "⌃↵ to tag all tabs across all windows",
            "variables": {
                "tag_all_tabs": "1",
                "tag_all_windows": "1"
            }
        }
    }
} for tag in filtered]

if not items:
    items = [{
        "title": "No matching tags",
        "valid": False
    }]

print(json.dumps({"items": items}))
