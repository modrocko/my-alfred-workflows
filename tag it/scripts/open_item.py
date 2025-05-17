import sys
import os
import json
import subprocess
import urllib.parse

# get tag & uid from $1
#tag, uid = sys.argv[1].strip().split("||")
#print(f"tag={tag}\nuid={uid}", file=sys.stderr)

tag=os.environ["tag"]
uid=os.environ["uid"]

# load items.json
data_path = os.path.join(os.environ["alfred_workflow_data"], "items.json")
with open(data_path) as f:
    data = json.load(f)

# find the right block & entry
block = next((b for b in data if b.get("tag") == tag), {})
entry = next((e for e in block.get("items", []) if e.get("uid") == uid), {})

# decide how to open
item_type = entry.get("type", "")
if item_type == "email":
    message_id = entry.get("id", "")
    encoded = urllib.parse.quote(f"<{message_id}>")
    subprocess.run(["open", f"message://{encoded}"])

elif item_type == "file":
    path = entry.get("path", "")
    subprocess.run(["open", path])

elif item_type == "bookmark":
    url = entry.get("url", "")
    subprocess.run(["open", url])
