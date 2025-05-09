import os
import sys
import json
import subprocess

# Get args
raw = sys.argv[1].strip()
try:
    tag, item_id, item_type = [x.strip().replace("!", "❗") for x in raw.split("||")]
except:
    print("Invalid input format")
    sys.exit(1)

# Paths
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
title = os.environ.get("alfred_workflow_name", "TagIt")

# Load data
if not os.path.exists(items_path):
    sys.exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

# Process blocks
updated = False
for block in data:
    if block.get("tag") != tag:
        continue

    original = block.get("items", [])
    if item_id:
        filtered = [i for i in original if i.get("id") != item_id]
    else:
        filtered = [i for i in original if i.get("type") != item_type]

    if len(filtered) != len(original):
        if filtered:
            block["items"] = filtered
        else:
            block["items"] = []
        updated = True

# Remove empty tag blocks
data = [b for b in data if b.get("items")]

# Save back
if updated:
    with open(items_path, "w") as f:
        json.dump(data, f, indent=2)

    what = "item" if item_id else f"all {item_type}s"
    msg = f"Removed {what} from {tag}"
    subprocess.run([
        "osascript", "-e",
        f'display notification \"{msg}\" with title \"{title}\"'
    ])
