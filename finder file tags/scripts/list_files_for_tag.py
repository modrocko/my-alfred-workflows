import os
import sys
import json

tag = sys.argv[1].strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    files = json.load(f)

items = []
for entry in files:
    if entry.get("tag") == tag:
        for path in entry.get("paths", []):
            items.append({
                "title": os.path.basename(path.rstrip("/")),
                "subtitle": path,
                "arg": path,
                "mods": {
                    "cmd": {
                        "arg": f"{path}||{tag}",
                        "subtitle": f"⌘↵ to remove tag '{tag}' from this file"
                    },
                    "alt": {
                        "arg": path,
                        "subtitle": f"⌥↵ to open & remove tag '{tag}'",
                        "variables": {
                            "tag": tag
                        }
                    },
                    "ctrl": {
                        "arg": "reassign",
                        "subtitle": f"⌃↵ to reassign tag from '{tag}'",
                        "variables": {
                            "path": path,
                            "old_tag": tag
                        }
                    },
                    "shift": {
                        "arg": path,
                        "subtitle": f"⇧↵ to reveal in Finder"
                    }
                }
            })

print(json.dumps({"items": items}))
