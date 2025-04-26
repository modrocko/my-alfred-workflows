import os
import sys
import json
import subprocess

tag = sys.argv[1].strip().replace("!", "❗")
if not tag:
    sys.exit(0)

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")
title = os.environ["alfred_workflow_name"]

# AppleScript → get POSIX paths of selected files in Finder
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

# No files selected
if not raw_output:
    subprocess.run([
        "osascript", "-e",
        f'display notification "No file(s) selected. Select file(s) to tag." with title "{title}"'
    ])
    sys.exit(0)

# Parse paths
paths = [item.strip() for item in raw_output.split("%%") if item.strip()]

# Load or create db
if os.path.exists(db_path):
    with open(db_path, "r") as f:
        db = json.load(f)
else:
    db = []

# Tag files - add entry only if path+tag combo doesn't exist
added = 0
for path in paths:
    already_tagged = any(
        entry["tag"] == tag and path in entry.get("paths", [])
        for entry in db
    )
    if not already_tagged:
        # Check if tag already exists
        tag_entry = next((entry for entry in db if entry["tag"] == tag), None)
        if tag_entry:
            tag_entry["paths"].append(path)
        else:
            db.append({
                "tag": tag,
                "paths": [path]
            })
        added += 1

# Save db
with open(db_path, "w") as f:
    json.dump(db, f, indent=2)

# Notify
notif_text = f"Tagged {added} file{'s' if added != 1 else ''} with '{tag}'"
subprocess.run([
    "osascript", "-e",
    f'display notification \"{notif_text}\" with title \"{title}\"'
])

print(f"✅ {notif_text}")
