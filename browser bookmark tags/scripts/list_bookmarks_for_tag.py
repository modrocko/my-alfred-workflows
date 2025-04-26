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

items = []
for bm in bookmarks:
    if tag in bm.get("tags", []):
        title = bm.get("title", "")
        url = bm.get("url", "")
        items.append({
            "title": title,
            "subtitle": url,
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
