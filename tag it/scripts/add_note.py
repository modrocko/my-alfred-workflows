import os
import sys
import json
import uuid
import subprocess

# 1) Parse tag & note from $1
tag, note_text = sys.argv[1].replace("!", "❗").split("||", 1)
print(f"tag={tag}\nnote={note_text}", file=sys.stderr)

title = os.environ["alfred_workflow_name"]

# 2) Load JSON data
data_path = os.path.join(os.environ["alfred_workflow_data"], "items.json")
if os.path.exists(data_path):
    with open(data_path, "r") as f:
        data = json.load(f)
else:
    data = []

# 3) Find existing tag block only
block = next((b for b in data if b.get("tag") == tag), None)
if not block:
    # nothing to do if tag not found
    sys.exit(0)

# 4) Append new note entry
new_entry = {
    "type": "note",
    "uid": str(uuid.uuid4()),
    "note": note_text
}
block["items"].append(new_entry)

# 5) Save back to items.json
with open(data_path, "w") as f:
    json.dump(data, f, indent=2)

# 6) Post notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Note added to {tag}" with title "{title}"'
])
