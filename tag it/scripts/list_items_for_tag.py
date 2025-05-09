import os
import sys
import json

# Get incoming values
query_tag = sys.argv[1].split("||")[-1].strip().replace("!", "❗").lower()
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
#items = [{
#    "title": "Keyboard shortcuts",
#    "subtitle": "↵ Open • ⌘ Remove item • ⌥ Rename title",
#    "valid": False,
#    "icon": { "path": "icons/info.png" }
#}]

for entry in block["items"]:
    item_type = entry.get("type")
    note = entry.get("note", "")
    subtitle = ""
    title = ""
    arg = ""
    icon = {}

    if filter_type and filter_type != "all" and item_type != filter_type:
        continue

    if item_type == "email":
        uid = entry.get("uid", "")
        title = entry.get("subject", "(No Subject)")
        sender = entry.get("sender", "")
        date = entry.get("date", "")
        message_id = entry.get("id", "")
        subtitle = f"[email] ∙ {sender} • {date}"
        arg = f"{message_id}||{query_tag}"
        icon = { "path": os.path.join(workflow_dir_root, "icons/email.png") }

    elif item_type == "file":
        uid = entry.get("uid", "")
        path = entry.get("path", "")
        title = entry.get("name") or os.path.basename(path.rstrip("/"))
        kind = "folder" if os.path.isdir(path) else "file"
        subtitle = f"[{kind}] • {path}"
        arg = f"{path}||{query_tag}"
        icon = { "path": "icons/file.png" }

    elif item_type == "bookmark":
        uid = entry.get("uid", "")
        title = entry.get("title", entry.get("url", ""))
        url = entry.get("url", "")
        subtitle = f"[bookmark] • {url}"
        arg = f"{url}||{query_tag}"
        icon = { "path": os.path.join(workflow_dir_root, "icons/bookmark.png") }

    else:
        continue  # Skip unknown types

    items.append({
        "uid": uid,
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": True,
        "variables": {
            "action": "open",
            "item_type": item_type,
            "tag": query_tag
        },
        "icon": icon,
        "mods": {
            "cmd": {
                "subtitle": "⌘ Remove item",
                "arg": query_tag,
                "variables": {
                    "uid": uid
                }
            },
            "alt": {
                "subtitle": "⌥ Rename title",
                "arg": title,
                "variables": {
                    "tag": query_tag,
                    "uid": uid,
                    "old_title": title
                }
              }
            }
        })


items.sort(key=lambda x: x["title"].lower())

print(json.dumps({ "items": items }))
