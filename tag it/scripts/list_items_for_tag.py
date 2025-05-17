import os
import sys
import json
import urllib.parse

# Get incoming values
query_tag = sys.argv[1].split("||")[-1].strip().replace("!", "❗")
filter_type = os.environ.get("item_type")

print("filter type:", filter_type, file=sys.stderr)

# Set up paths
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
workflow_dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load tagged data
if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

# Find tag block
block = next((b for b in data if b.get("tag") == query_tag), None)
if not block or not block.get("items"):
    print(json.dumps({ "items": [] }))
    exit(0)

items = []
for entry in block["items"]:
    item_type = entry.get("type")
    uid = entry.get("uid", "")
    subtitle = ""
    title = ""
    arg = ""
    icon = {}

    if filter_type and filter_type != "all" and item_type != filter_type:
        continue

    if item_type == "email":
        title = entry.get("subject", "(No Subject)")
        sender = entry.get("sender", "")
        date = entry.get("date", "")
        message_id = entry.get("id", "")
        subtitle = f"[email] ∙ {sender} • {date}"
        path = "message://" + urllib.parse.quote(f"<{message_id}>")
        icon = { "path": "icons/email.png" }

    elif item_type == "file":
        path = entry.get("path", "")
        title = entry.get("name") or os.path.basename(path.rstrip("/"))
        kind = "folder" if os.path.isdir(path) else "file"
        subtitle = f"[{kind}] • {path}"
        icon = { "path": "icons/file.png" }

    elif item_type == "bookmark":
        title = entry.get("title", entry.get("url", ""))
        url = entry.get("url", "")
        subtitle = f"[bookmark] • {url}"
        path = url
        icon = { "path": "icons/bookmark.png" }

    elif item_type == "note":
        path = entry.get("path", "")
        title = entry.get("name") or os.path.basename(path.rstrip("/"))
        kind = "folder" if os.path.isdir(path) else "note"
        subtitle = f"[{kind}] • {path}"
        icon = { "path": "icons/note.png" }

    else:
        continue  # Skip unknown types

    items.append({
        "uid": uid,
        "title": title,
        "subtitle": subtitle,
        "arg": path,
        "icon": icon,
        "variables": {
            "tag": query_tag,
            "uid": uid,
            "caller": "list_items"
        },
        "mods": {
            "cmd": {
                "subtitle": "⌘ Remove item",
                "arg": f"{query_tag}||{uid}",
                "variables": {
                    "caller": "list_items"
                }
            },
            "alt": {
                "subtitle": "⌥ Rename title",
                "arg": title,
                "variables": {
                    "tag": query_tag,
                    "uid": uid,
                    "old_title": title,
                    "caller": "list_items"
                }
              }
            }
        })


items.sort(key=lambda x: x["title"].lower())

print(json.dumps({ "items": items }))
