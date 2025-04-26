import os
import sys
import json

query = sys.argv[1].replace("!", "❗").lower() if len(sys.argv) > 1 else ""

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")
default_tags_path = os.path.join(workflow_dir, "default-tags.json")

# Load tasks
tasks = []
if os.path.exists(db_path):
    with open(db_path, "r") as f:
        tasks = json.load(f)

# Load default tags
default_tags = []
if os.path.exists(default_tags_path):
    with open(default_tags_path, "r") as f:
        default_tags = json.load(f)

# Gather all tags
tag_set = set(default_tags)
for task in tasks:
    tag_set.add(task.get("tag", ""))

# Filter tags by query
filtered = sorted(t for t in tag_set if query in t.lower())

# Include typed input if not already present
if query and query not in [t.lower() for t in tag_set]:
    filtered.insert(0, query)

# Build Alfred results
items = []
for tag in filtered:
    items.append({
        "title": tag,
        "subtitle": "↵ to add new task (format: <tag> | <task>) • ⌘ prefill with tag",
        "arg": tag,
        "mods": {
            "cmd": {
                "arg": f"{tag} | ",
                "subtitle": "⌘↵ to prefill with tag",
                "valid": True
            }
        }
    })

print(json.dumps({ "items": items }))
