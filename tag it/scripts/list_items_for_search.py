import os
import sys
import json
import urllib.parse
from utils import get_bookmark_icon

query = sys.argv[1].strip().replace("!", "❗").lower() if len(sys.argv) > 1 else ""
print(f"QUERY: {query}", file=sys.stderr)

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    tag_groups = json.load(f)

items = [{
    "title": "Keyboard shortcuts",
    "subtitle": "↵ Open • ⌘ Remove item • ⌥ Rename title",
    "valid": False,
    "icon": { "path": "icons/info.png" }
}]

bookmark_icon = get_bookmark_icon()

for group in tag_groups:
    tag = group.get("tag", "")

    for item in group.get("items", []):
        type_ = item.get("type", "")
        label = ""
        subtitle_detail = ""
        arg = ""
        uid = item.get("uid", "")
        icon = {}

        if type_ == "file":
            path = item.get("path", "")
            title = item.get("name") or os.path.basename(path.rstrip("/"))
            label = title
            subtitle_detail = path
            icon = { "path": path, "type": "fileicon" }

        elif type_ == "email":
            label = item.get("subject", "")
            sender = item.get("sender", "")
            date = item.get("date", "")
            subtitle_detail = f"{sender} • {date}"
            message_id = item.get("id", "")
            path = "message://" + urllib.parse.quote(f"<{message_id}>")
            icon = {"path": "/System/Applications/Mail.app", "type": "fileicon"}

        elif type_ == "bookmark":
            label = item.get("title") or item.get("url", "")
            url = item.get("url", "")
            subtitle_detail = url
            path = url
            #icon = { "path": "icons/bookmark.png" }
            icon = bookmark_icon

        else:
            continue  # skip unknown types

        if not any(query in (x or "").lower() for x in [tag, label, type_, subtitle_detail]):
            continue

        subtitle = f"[{tag}] • {subtitle_detail}"

        items.append({
            "title": label,
            "subtitle": subtitle,
            "arg": path,
            "icon": icon,
            "variables": {
                "tag": tag,
                "uid": uid,
                "caller": "search_tags"
            },
            "mods": {
                "cmd": {
                    "subtitle": "⌘ Remove item",
                    "arg": f"{tag}||{uid}",
                    "variables": {
                        "caller": "search_tags"
                    }
                },
                "alt": {
                    "subtitle": "⌥ Rename title",
                    "arg": label,
                    "variables": {
                        "tag": tag,
                        "uid": uid,
                        "old_title": label,
                        "caller": "search_tags"
                }
              }
            }
        })

# Fallback if no match
if len(items) == 1:
    items = [{
        "title": "No matches found",
        "subtitle": "So tag some!",
        "valid": False,
        "icon": { "path": "icons/info.png" }
    }]

print(json.dumps({ "items": items }))
