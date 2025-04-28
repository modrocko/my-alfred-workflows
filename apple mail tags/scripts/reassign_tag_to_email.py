import os
import sys
import json
import subprocess

new_tag = sys.argv[1].strip().replace("!", "❗")
message_id = os.environ.get("id", "").strip()
old_tag = os.environ.get("old_tag", "").strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
notif_title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    print("Data file not found")
    sys.exit(1)

with open(db_path, "r") as f:
    emails = json.load(f)

changed = False

# Find old tag group
old_tag_entry = next((b for b in emails if b.get("tag") == old_tag), None)

# Find or create new tag group
new_tag_entry = next((b for b in emails if b.get("tag") == new_tag), None)
if not new_tag_entry:
    new_tag_entry = {"tag": new_tag, "emails": []}
    emails.append(new_tag_entry)

# Move email from old to new
if old_tag_entry:
    for entry in old_tag_entry.get("emails", []):
        if entry.get("id") == message_id:
            new_tag_entry["emails"].append(entry)
            old_tag_entry["emails"].remove(entry)
            changed = True
            break

# Clean up any empty tag groups
emails = [b for b in emails if b.get("emails")]

if changed:
    with open(db_path, "w") as f:
        json.dump(emails, f, indent=2)

    print(f"✅ Reassigned tag '{old_tag}' → '{new_tag}'")

    notif_text = f"Email reassigned from '{old_tag}' to '{new_tag}'"
    subprocess.run([
        "osascript", "-e",
        f'display notification "{notif_text}" with title "{notif_title}"'
    ])
else:
    print("❌ Email not found or tag not changed")
