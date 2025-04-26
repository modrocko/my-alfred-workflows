import os
import sys
import json
import subprocess

# Get tag from input
tag = sys.argv[1].strip()

# Load file data
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")

if not os.path.exists(db_path):
    sys.exit()

with open(db_path, "r") as f:
    data = json.load(f)

# Open each matching file
for entry in data:
    if entry.get("tag") == tag:
        for path in entry.get("paths", []):
            subprocess.run(["open", path])
