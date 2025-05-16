import os
import sys
import json

query_tag = sys.argv[1].strip().replace("!", "❗")

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

# Load data
if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

# Get block for the tag
block = next((b for b in data if b.get("tag") == query_tag), None)
if not block or not block.get("items"):
    print(json.dumps({ "items": [] }))
    exit(0)

# Group counts by type
counts = {
    "email": [],
    "bookmark": [],
    "file": [],
    "note": []
}

for item in block["items"]:
    item_type = item.get("type")
    if item_type in counts:
        counts[item_type].append(item)

# Build output list
items = []
items.append({
    "title": "View all items",
    "subtitle": f"{query_tag}",
    "arg": query_tag,
    "variables": {
        "item_type": "all",
        "tag": query_tag
    }
})

# Mapping per type
labels = {
    "email": "Emails",
    "bookmark": "Bookmarks",
    "file": "Files",
    "note": "Notes"
}

icons = {
    "email": "icons/email.png",
    "bookmark": "icons/bookmark.png",
    "file": "icons/file.png",
    "note": "icons/note.png"
}

for item_type, group in counts.items():
    if not group:
        continue

    label = labels[item_type]
    count = len(group)
    icon = icons[item_type]

    items.append({
        "title": f"{count} {label}",
        "subtitle": f"↵ View • ⌘ Tag {item_type}s • ⌥ Remove {item_type}s • ⌃ Open all {item_type}s",
        "arg": query_tag,
        "variables": {
            "item_type": item_type
        },
        "icon": { "path": icon },
        "mods": {
            "cmd": {
                "subtitle": "⌘ Tag new items",
                "arg": query_tag,
                "variables": {
                    "item_type": item_type,
                    "tag": query_tag,
                    "variables":{ "action":"tag_items" }
                }
            },
            "alt": {
                "subtitle": "⌥ Remove items",
                "arg": f"{query_tag}||||{item_type}",
                "variables": {}
            },
            "ctrl": {
                "subtitle": "⌃ Open all",
                "arg": f"{query_tag}||{item_type}",
                "variables": {}
            }
        }
    })

print(json.dumps({ "items": items }))
