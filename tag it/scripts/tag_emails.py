import os
import sys
import json
import subprocess
import uuid

tag = sys.argv[1].strip().replace("!", "❗")
if not tag:
    sys.exit(0)

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
title = os.environ["alfred_workflow_name"]

# AppleScript to get selected email details, including message ID
applescript = """
tell application "Mail"
	set selectedMessages to selection
	set output to ""
	repeat with msg in selectedMessages
		set theSubject to subject of msg
		set theSender to sender of msg
		set theDate to date received of msg
		set theID to message id of msg
		set output to output & theSubject & "||" & theSender & "||" & theDate & "||" & theID & "%%"
	end repeat
	return output
end tell
"""

result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
raw_output = result.stdout.strip()

if not raw_output:
    subprocess.run([
        "osascript",
        "-e",
        f'display notification "No mail(s) selected. Select mail(s) to tag." with title "{title}"'
    ])
    sys.exit(0)

# Parse result into email items
emails = []
for entry in raw_output.split("%%"):
    if not entry.strip():
        continue
    parts = entry.strip().split("||")
    if len(parts) == 4:
        emails.append({
            "type": "email",
            "subject": parts[0].strip(),
            "sender": parts[1].strip(),
            "date": parts[2].strip(),
            "id": parts[3].strip(),
            "uid": str(uuid.uuid4())
        })

# Load items.json
if os.path.exists(items_path):
    with open(items_path, "r") as f:
        data = json.load(f)
else:
    data = []

# Find or create tag block
tag_block = next((b for b in data if b.get("tag") == tag), None)
if not tag_block:
    tag_block = { "tag": tag, "items": [] }
    data.append(tag_block)

# Add new emails if not already present
added = 0
for email in emails:
    exists = any(
        item["type"] == "email" and
        item.get("id") == email["id"]
        for item in tag_block["items"]
    )
    if not exists:
        tag_block["items"].append(email)
        added += 1

# Save items.json
with open(items_path, "w") as f:
    json.dump(data, f, indent=2)

# Notify user
subprocess.run([
    "osascript", "-e",
    f'display notification "Tagged {added} email(s) with \\"{tag}\\"" with title "{title}"'
])
