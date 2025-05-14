import os
import json
import sys

query = sys.argv[1].lower() if len(sys.argv) > 1 else ""
query = query.replace("!", "❗")

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

# Load data
if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

# Build tag summary
items = []
for block in data:
    tag = block.get("tag", "")
    type_counts = { "email": 0, "file": 0, "bookmark": 0 }

    for item in block.get("items", []):
        t = item.get("type")
        if t in type_counts:
            type_counts[t] += 1

    # Skip tags with no items
    if not any(type_counts.values()):
        continue

    # Build summary string like: [2 emails, 4 bookmarks, 1 file]
    type_labels = []
    if type_counts["email"]:
        type_labels.append(f'{type_counts["email"]} email{"s" if type_counts["email"] > 1 else ""}')
    if type_counts["bookmark"]:
        type_labels.append(f'{type_counts["bookmark"]} bookmark{"s" if type_counts["bookmark"] > 1 else ""}')
    if type_counts["file"]:
        type_labels.append(f'{type_counts["file"]} file{"s" if type_counts["file"] > 1 else ""}')

    subtitle = f"[{', '.join(type_labels)}] • ↵ View tag(s) • ⌘ Rename tag • ⌥ Remove tag • ⌃ View items"

    if query in tag.lower():
        items.append({
            "title": tag,
            "subtitle": subtitle,
            "arg": tag,
            "mods": {
                "cmd": {
                    "subtitle": "⌘ Rename tag",
                    "arg": tag,
                    "variables": {
                        "old_tag": tag
                    }
                },
                "alt": {
                    "subtitle": "⌥ Remove tag",
                    "arg": tag
                },
                "ctrl": {
                    "subtitle": "⌃ View items",
                    "arg": tag
                }
            }
        })

# If no items matched, show fallback
if not items:
    items.append({
        "title": "No matches found",
        "subtitle": "So then tag some, silly",
        "valid": False,
        "icon": { "path": "icons/info.png" }
    })

items.sort(key=lambda x: x["title"].lower())
print(json.dumps({ "items": items }))
