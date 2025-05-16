import sys
import os
import json

query = sys.argv[1].strip().replace("!", "❗") if len(sys.argv) > 1 else ""

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

if not query:
    items = [{
        "title": "Specify tag",
        "subtitle": "Type or select a tag",
        "valid": False,
        "icon": { "path": "icons/info.png" }
    }]
else:
    items = []

# Load existing tags
tags = []
if os.path.exists(items_path):
    with open(items_path, "r") as f:
        data = json.load(f)
        tags = sorted(set(b["tag"] for b in data if b.get("tag")))

# Base mod block (include tag + item_type)
def build_mods(tag):
    return {
        "cmd": {
            "valid": True,
            "arg": tag,
            "subtitle": "⌘ Tag files",
            "variables": {
                "item_type": "file",
                "tag": tag
            }
        },
        "alt": {
            "valid": True,
            "arg": tag,
            "subtitle": "⌥ Tag browser tabs",
            "variables": {
                "item_type": "bookmark",
                "tag": tag
            }
        },
        "ctrl": {
            "valid": True,
            "arg": tag,
             "subtitle": "⌃ Tag notes",
             "variables": {
                 "item_type": "note",
                 "tag": tag
             }
        }
    }

# Suggest new tag entry
if query and query not in tags:
    items.append({
        "title": f"'{query}'",
        "subtitle": "↵ Tag emails • ⌘ Tag files • ⌥ Tag browser tabs • ⌃ Tag notes",
        "arg": query,
        "variables": {
            "item_type": "email",
            "tag": query
        },
        "mods": build_mods(query)
    })

# Show matching existing tags
for tag in tags:
    if query.lower() not in tag.lower():
        continue
    items.append({
        "title": tag,
        "subtitle": "↵ Tag emails • ⌘ Tag files • ⌥ Tag browser tabs • ⌃ Tag notes",
        "arg": tag,
        "variables": {
            "item_type": "email",
            "tag": tag
        },
        "mods": build_mods(tag)
    })

print(json.dumps({ "items": items }))
