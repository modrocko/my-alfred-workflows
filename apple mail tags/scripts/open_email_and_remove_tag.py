import os
import json
import subprocess
import urllib.parse
import time

message_id = os.getenv("message_id")
tag = os.getenv("tag")

workflow_dir = os.environ["alfred_workflow_data"]
data_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

# 📨 Open the email in Mail
if message_id:
    encoded = urllib.parse.quote(f"<{message_id}>")
    url = f"message://{encoded}"
    subprocess.run(["open", url])

# ⏱ Add a short delay so Mail has time to open the message
time.sleep(0.5)

tag_removed = False

if os.path.exists(data_path):
    with open(data_path, "r") as f:
        emails = json.load(f)

    # Find the tag group
    for tag_entry in emails:
        if tag_entry.get("tag") == tag:
            original_count = len(tag_entry["emails"])
            tag_entry["emails"] = [entry for entry in tag_entry["emails"] if entry.get("id") != message_id]
            if len(tag_entry["emails"]) != original_count:
                tag_removed = True
            break

    # Remove the tag group if it has no emails left
    emails = [b for b in emails if b.get("emails")]

    with open(data_path, "w") as f:
        json.dump(emails, f, indent=2)

# ✅ Show notification
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Removed tag \\"{tag}\\" from email." with title "{title}"'
    ])
