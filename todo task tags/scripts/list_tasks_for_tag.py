import os
import sys
import json

tag = sys.argv[1].strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")

# Load data
if not os.path.exists(db_path):
    print(json.dumps({ "items": [] }))
    sys.exit(0)

with open(db_path, "r") as f:
    data = json.load(f)

# Find tasks for this tag
entry = next((e for e in data if e.get("tag") == tag), None)

if not entry or not entry.get("tasks"):
    print(json.dumps({ "items": [] }))
    sys.exit(0)

tasks = entry["tasks"]

# Build results
items = []
for task in tasks:
    items.append({
        "title": task,
        "arg": "reassign",
        "subtitle": f"{tag} ∙ ↵ reassign tag ∙ ⌘↵ update task ∙ ⌥↵ complete task ∙ ⌃↵ remove task",
        "variables": {
            "task": task,
            "old_tag": tag
        },
        "mods": {
            "cmd": {
                "subtitle": "⌘↵ to update task",
                "arg": task,
                "variables": {
                    "tag": tag,
                    "old_task": task
                }
            },
            "alt": {
                "subtitle": "⌥↵ to mark as completed",
                "arg": "✅ " + task,
                "variables": {
                    "tag": tag,
                    "old_task": task
                }
            },
            "ctrl": {
                "subtitle": "⌃↵ to remove task",
                "arg": f"{tag}||{task}",
                "variables": {
                    "action": "remove"
                }
            }
        }
    })

print(json.dumps({ "items": items }))