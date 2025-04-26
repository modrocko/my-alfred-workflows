import os
import sys
import json

query = sys.argv[1].strip().lower()
query = query.replace("!", "❗")

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    tasks_data = json.load(f)

results = []
for entry in tasks_data:
    tag = entry.get("tag", "")
    for task in entry.get("tasks", []):
        if query in task.lower() or query in tag.lower():
            results.append({
                "title": task,
                "subtitle": f"[{tag}] •  ↵ update task • ⌘ complete task • ⌥ remove task • ⌃ reassign task",
                "arg": task,
                "variables": {
                    "tag": tag,
                    "old_task": task
                },
                "mods": {
                    "cmd": {
                        "arg": "✅ " + task,
                        "subtitle": "⌘↵ to mark as completed",
                        "variables": {
                            "tag": tag,
                            "old_task": task
                        }
                    },
                    "alt": {
                        "arg": f"{tag}||{task}",
                        "subtitle": "⌥↵ to remove task",
                        "variables": {
                            "action": "remove"
                        }
                    },
                    "ctrl": {
                        "arg": "reassign",
                        "subtitle": f"{tag} ∙ ↵ reassign tag",
                        "variables": {
                            "task": task,
                            "old_tag": tag
                        }
                    }
                }
            })

if not results:
    results.append({
        "title": "No matches found",
        "subtitle": f"No tasks found for: {query}",
        "valid": False
    })

print(json.dumps({"items": results}))
