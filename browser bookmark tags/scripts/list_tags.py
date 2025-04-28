import os
import sys
import json
import subprocess

# Get user input
query = sys.argv[1].lower() if len(sys.argv) > 1 else ""
query = query.replace("!", "❗")

# Resolve paths
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")

# If no file exists, return empty
if not os.path.exists(db_path):
    print(json.dumps({"items": []}))
    sys.exit(0)

# Load bookmarks
with open(db_path, "r") as f:
    bookmarks = json.load(f)

# Count number of URLs per tag
tag_counts = {}
for bm in bookmarks:
    tag = bm.get("tag", "")
    urls = bm.get("urls", [])
    if tag:
        tag_counts[tag] = len(urls)

# Filter by query
filtered_tags = sorted(tag for tag in tag_counts if query in tag.lower()) if query else sorted(tag_counts)

# Build results
items = []
for tag in filtered_tags:
    count = tag_counts[tag]
    items.append({
        "title": tag,
        "subtitle": f"{count} bookmark{'s' if count != 1 else ''} • ↵ view • ⌘ remove • ⌥ rename • ⌃ tag • ⇧ view all • ⌃⇧ tag all",
        "arg": tag,
        "mods": {
            "cmd": {
                "arg": tag,
                "subtitle": f"⌘↵ to remove tag: {tag}"
            },
            "alt": {
                "arg": tag,
                "subtitle": f"⌥↵ to rename tag: {tag}",
                "variables": {
                    "old_tag": tag
                }
            },
            "ctrl": {
                "arg": tag,
                "subtitle": f"⌃↵ to tag current tab with: {tag}"
            },
            "shift": {
                "arg": tag,
                "subtitle": f"⇧↵ to open all tabs with: {tag}"
            },
            "ctrl+shift": {
                "arg": tag,
                "subtitle": f"⌃⇧↵ to tag all tabs with: {tag}",
                "variables": {
                    "tag_all_tabs": "1"
                }
            }
        }
    })


if not items:
    items = [{
        "title": "No tagged bookmarks found",
        "valid": False
    }]

# Output to Alfred
print(json.dumps({"items": items}))
