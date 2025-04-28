import os
import sys
import json
import subprocess
import urllib.parse

tag = sys.argv[1].strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")

if not os.path.exists(db_path):
    sys.exit()

with open(db_path, "r") as f:
    emails = json.load(f)

# Find the tag group
tag_entry = next((b for b in emails if b.get("tag") == tag), None)

# Open all emails under that tag
if tag_entry:
    for entry in tag_entry.get("emails", []):
        message_id = entry.get("id")
        if message_id:
            encoded = urllib.parse.quote(f"<{message_id}>")
            url = f"message://{encoded}"
            subprocess.run(["open", url])
