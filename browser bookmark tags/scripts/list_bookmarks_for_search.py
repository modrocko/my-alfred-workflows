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
    title = bm.get("title", "")
    url = bm.get("url", "")
    tags_list = bm.get("tags", [])
    tag = tags_list[0] if tags_list else ""

    if (
        query in title.lower()
        or query in url.lower()
        or any(query in t.lower() for t in tags_list)
    ):
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
