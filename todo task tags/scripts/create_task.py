import os
import sys
import json
import subprocess

# Get input
raw = sys.argv[1].strip()

# Must contain '|'
if "|" not in raw:
    subprocess.run([
        "osascript", "-e",
        'display notification "Use format: <tag> | <task>" with title "To-Do task not added"'
    ])
    sys.exit(0)

# Split input
tag, task = map(lambda s: s.strip().replace("!", "❗"), raw.split("|", 1))

# File path
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")

# Exit if file missing
if not os.path.exists(db_path):
    sys.exit(0)

# Load tasks
with open(db_path, "r") as f:
    data = json.load(f)

# Track if task was added
added = False

# Find tag entry or create one
for entry in data:
    if entry["tag"] == tag:
        if task not in entry["tasks"]:
            entry["tasks"].append(task)
            added = True
        break
else:
    data.append({
        "tag": tag,
        "tasks": [task]
    })
    added = True

# Save back
with open(db_path, "w") as f:
    json.dump(data, f, indent=2)

# Notification
notif_text = f"Added: {task}" if added else f"Task already exists: {task}"
subprocess.run([
    "osascript", "-e",
    f'display notification "{notif_text}" with title "To-Do Task Created"'
])

print(f"✅ {notif_text} [{tag}]")
