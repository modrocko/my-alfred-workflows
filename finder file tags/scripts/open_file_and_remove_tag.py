import os
import json
import subprocess

path = os.getenv("path")
tag = os.getenv("tag")

workflow_dir = os.environ["alfred_workflow_data"]
data_path = os.path.join(workflow_dir, "files.json")
title = os.environ["alfred_workflow_name"]

tag_removed = False
updated_files = []

if os.path.exists(data_path):
    with open(data_path, "r") as f:
        files = json.load(f)

    for item in files:
        if path in item.get("paths", []):
            if tag == item.get("tag"):
                item["paths"].remove(path)
                tag_removed = True
            if item["paths"]:
                updated_files.append(item)
            # skip if no paths left
        else:
            updated_files.append(item)

    with open(data_path, "w") as f:
        json.dump(updated_files, f, indent=2)

# ✅ Notification
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Removed tag \\"{tag}\\" from file." with title "{title}"'
    ])

# Open file
subprocess.run(["open", path])
