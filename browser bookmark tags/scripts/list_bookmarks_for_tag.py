import os
import sys
import json

tag = sys.argv[1].strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")

if not os.path.exists(db_path):
    print(json.dumps({"items": []}))
    sys.exit(0)

with open(db_path, "r") as f:
    bookmarks = json.load(f)

# Find the tag group
tag_entry = next((b for b in bookmarks if b.get("tag") == tag), None)

items = []
if tag_entry:
    for entry in tag_entry.get("urls", []):
        title = entry.get("title", "")
        url = entry.get("url", "")

        items.append({
            "title": title,
            "subtitle": f"[{tag}] • {url}",
            "arg": url,
            "mods": {
                "cmd": {
                    "arg": f"{url}||{tag}",
                    "subtitle": f"⌘↵ to remove tag '{tag}' from this bookmark"
                },
                "alt": {
                    "arg": url,
                    "subtitle": f"⌥↵ to open & remove tag '{tag}'",
                    "variables": {
                        "tag": tag
                    }
                },
                "ctrl": {
                    "arg": "reassign",
                    "subtitle": f"⌃↵ to reassign tag from '{tag}'",
                    "variables": {
                        "url": url,
                        "old_tag": tag
                    }
                }
            }
        })

print(json.dumps({"items": items}))
