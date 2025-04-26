import os
import json
import sys

# Get typed input from Alfred
query = sys.argv[1].lower() if len(sys.argv) > 1 else ""

# Get workflow directory path
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "tasks.json")

# Return nothing if file doesn't exist
if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

# Load tasks
with open(db_path, "r") as f:
    tasks = json.load(f)

# Count how many tasks per tag
tag_counts = {entry["tag"]: len(entry.get("tasks", [])) for entry in tasks}

# Filter & sort tags
filtered_tags = sorted(tag for tag in tag_counts if query in tag.lower()) if query else sorted(tag_counts)

# Show fallback if nothing matches
if not filtered_tags:
    print(json.dumps({
        "items": [{
            "title": "No matches found",
            "subtitle": f"No tags found for: {query}",
            "valid": False
        }]
    }))
    exit()

# Build Alfred results
items = []
for tag in filtered_tags:
    count = tag_counts[tag]
    items.append({
        "title": tag,
        "subtitle": f"{count} task{'s' if count != 1 else ''} ∙ ↵ view all ∙ ⌘ create task ∙ ⌥ rename tag ∙ ⌃ remove tag",
        "arg": tag,
        "mods": {
            "cmd": {
              "arg": tag + " | ",
              "subtitle": "⌘↵ to create new task for this tag"
            },
            "alt": {
                "arg": tag,
                "subtitle": f"⌥↵ to rename tag: {tag}",
                "variables": {
                    "action": "rename",
                    "old_tag": tag
                }
            },
            "ctrl": {
                "arg": tag,
                "subtitle": f"⌃↵ to remove tag: {tag}",
                "variables": {
                    "action": "remove"
                }
            }
        }
    })

# Output to Alfred
print(json.dumps({"items": items}))
