import os
import sys
import json
import subprocess

# split single arg into parts
#tag, uid, old_title, new_title = sys.argv[1].split("||")
tag, uid, old_title, new_title = sys.argv[1].replace("!", "❗").split("||")

print(f"tag={tag}\nuid={uid}\nold_title={old_title}\nnew_title={new_title}", file=sys.stderr)

workflow_dir = os.environ["alfred_workflow_data"]
path = os.path.join(workflow_dir, "items.json")

with open(path, "r") as f:
    data = json.load(f)

# find the right tag block
block = next((b for b in data if b.get("tag") == tag), None)
if not block:
    sys.exit(1)

# find the item by uid
item = next((i for i in block.get("items", []) if i.get("uid") == uid), None)
if not item:
    sys.exit(1)

# pick correct field by type
field = {
    "email": "subject",
    "bookmark": "title",
    "file": "name"
}.get(item.get("type"))

if field:
    item[field] = new_title

# save updates
with open(path, "w") as f:
    json.dump(data, f, indent=2)

# show a notification
title = os.environ.get("notification_title", "Tag Manager")
subprocess.run([
    "osascript", "-e",
    f'display notification "Title renamed from [{old_title}] to [{new_title}]" with title "{title}"'
])