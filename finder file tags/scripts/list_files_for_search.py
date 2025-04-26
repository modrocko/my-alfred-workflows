import os
import sys
import json

query = sys.argv[1].strip().lower()
query = query.replace("!", "❗")

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    files = json.load(f)

results = []
for entry in files:
    tag = entry.get("tag", "")
    for path in entry.get("paths", []):
        name = os.path.basename(path.rstrip("/"))
        if query in os.path.basename(path).lower() or query in path.lower() or query in tag.lower():
            results.append({
                "title": name,
                "subtitle": f"[{tag}] • {path}",
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
                        "subtitle": "⇧↵ to reveal in Finder"
                    }
                }
            })

if not results:
    results.append({
        "title": "No matches found",
        "subtitle": f"No files found for: {query}",
        "valid": False
    })

print(json.dumps({"items": results}))
