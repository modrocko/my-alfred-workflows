import os
import sys
import json
import subprocess

tag, uid = sys.argv[1].split("||")
print(f"TAG: {tag}\nUID: {uid}", file=sys.stderr)

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
notif_title = os.environ.get("alfred_workflow_name", "Tags")

if not os.path.exists(items_path):
    sys.exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

item_type = None
item_removed = False

for block in data:
    if block.get("tag") != tag:
        continue

    for item in block["items"]:
        if item.get("uid") == uid:
            item_type = item.get("type")
            break

    new_items = [item for item in block["items"] if item.get("uid") != uid]
    if len(new_items) != len(block["items"]):
        block["items"] = new_items
        item_removed = True
        break

if item_removed:
    # drop any tag blocks with no items left
    data = [b for b in data if b.get("items")]
    with open(items_path, "w") as f:
        json.dump(data, f, indent=2)

    if item_type:
        subprocess.run([
            "osascript", "-e",
            f'display notification "Removed {item_type} from \\"{tag}\\"" with title "{notif_title}"'
        ])
