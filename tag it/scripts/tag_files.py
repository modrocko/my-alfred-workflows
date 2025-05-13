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

# Get selected files via AppleScript
applescript = """
tell application "Finder"
	set selectedItems to selection
	set output to ""
	repeat with itemRef in selectedItems
		set itemPath to POSIX path of (itemRef as text)
		set output to output & itemPath & "%%"
	end repeat
	return output
end tell
"""

result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
raw_output = result.stdout.strip()

if not raw_output:
    subprocess.run([
        "osascript", "-e",
        f'display notification "No file(s) selected. Select file(s) to tag." with title "{title}"'
    ])
    sys.exit(0)

# Parse file paths
paths = [p.strip() for p in raw_output.split("%%") if p.strip()]

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

# Add new file items
added = 0
for path in paths:
    exists = any(
        item["type"] == "file" and item.get("path") == path
        for item in tag_block["items"]
    )
    if not exists:
        tag_block["items"].append({
            "type": "file",
            "path": path,
            "name": os.path.basename(path.rstrip("/")),
            "uid": str(uuid.uuid4())
        })
        added += 1

# Save items.json
with open(items_path, "w") as f:
    json.dump(data, f, indent=2)

# Notify
notif = f"Tagged {added} file{'s' if added != 1 else ''} with '{tag}'"
subprocess.run([
    "osascript", "-e",
    f'display notification \"{notif}\" with title \"{title}\"'
])

print(f"✅ {notif}")
