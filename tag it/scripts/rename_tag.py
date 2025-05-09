import os
import sys
import json
import subprocess

# Get and split input
arg = sys.argv[1].strip()
if "||" not in arg:
    print("Invalid input")
    sys.exit(1)

old_tag, new_tag = arg.split("||", 1)
old_tag = old_tag.strip()
new_tag = new_tag.strip().replace("!", "❗")

# Skip if no change
if not old_tag or not new_tag or old_tag == new_tag:
    print("No changes made")
    sys.exit(0)

# Load data
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
title = os.environ.get("alfred_workflow_name", "Workflow")

if not os.path.exists(items_path):
    print("Data file not found")
    sys.exit(1)

with open(items_path, "r") as f:
    data = json.load(f)

# Find matching tag blocks
old_block = None
new_block = None

for group in data:
    if group.get("tag") == old_tag:
        old_block = group
    elif group.get("tag") == new_tag:
        new_block = group

# Merge or rename
if old_block:
    if new_block:
        new_block["items"].extend(old_block["items"])
        data.remove(old_block)
    else:
        old_block["tag"] = new_tag

    with open(items_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Renamed {old_tag} → {new_tag}")

    subprocess.run([
        "osascript", "-e",
        f'display notification "Tag renamed from {old_tag} to {new_tag}." with title "{title}"'
    ])
else:
    print("Tag not found")
