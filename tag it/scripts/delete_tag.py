import os
import sys
import json
import subprocess

# Get tag from input
tag = sys.argv[1].strip().replace("!", "❗")
if not tag:
    print("No tag provided")
    sys.exit(1)

# Load items.json
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

if not os.path.exists(items_path):
    print("Data file not found")
    sys.exit(1)

with open(items_path, "r") as f:
    data = json.load(f)

# Remove block for the tag
new_data = [block for block in data if block.get("tag") != tag]

if len(new_data) == len(data):
    print("Tag not found")
    sys.exit(0)

# Save updated data
with open(items_path, "w") as f:
    json.dump(new_data, f, indent=2)

# Notify
title = os.environ.get("alfred_workflow_name", "TagIt")
subprocess.run([
    "osascript", "-e",
    f'display notification "Removed tag {tag}" with title "{title}"'
])
