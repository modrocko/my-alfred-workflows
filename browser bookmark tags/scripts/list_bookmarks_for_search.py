import os
import sys
import json

query = sys.argv[1].strip().lower()
query = query.replace("!", "❗")

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    bookmarks = json.load(f)

results = []
for bm in bookmarks:
    tag = bm.get("tag", "")
    for entry in bm.get("urls", []):
        title = entry.get("title", "")
        url = entry.get("url", "")

        if query in title.lower() or query in url.lower() or query in tag.lower():
            results.append({
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

if not results:
    results.append({
        "title": "No matches found",
        "subtitle": f"No bookmarks found for: {query}",
        "valid": False
    })

print(json.dumps({"items": results}))
