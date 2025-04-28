import os
import sys
import json

tag = sys.argv[1].strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    emails = json.load(f)

# Find the tag group
tag_entry = next((b for b in emails if b.get("tag") == tag), None)

items = []
if tag_entry:
    for entry in tag_entry.get("emails", []):
        subject = entry.get("subject", "")
        sender = entry.get("sender", "")
        date = entry.get("date", "")
        message_id = entry.get("id", "")
        items.append({
            "title": subject,
            "subtitle": f"{sender} — {date}",
            "arg": message_id,
            "mods": {
                "cmd": {
                    "arg": f"{message_id}||{tag}",
                    "subtitle": f"⌘↵ to remove tag '{tag}' from this email"
                },
                "alt": {
                    "arg": message_id,
                    "subtitle": f"⌥↵ to open & remove tag '{tag}'",
                    "variables": {
                        "tag": tag
                    }
                },
                "ctrl": {
                    "arg": "reassign",
                    "subtitle": f"⌃↵ to reassign tag from '{tag}'",
                    "variables": {
                        "id": message_id,
                        "old_tag": tag
                    }
                }
            }
        })

print(json.dumps({"items": items}))
