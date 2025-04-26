import os
import json
import sys

# Get typed input from Alfred
query = sys.argv[1].lower() if len(sys.argv) > 1 else ""

# Get workflow directory path
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "files.json")

# Return nothing if file doesn't exist
if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

# Load file tag data
with open(db_path, "r") as f:
    files = json.load(f)

# Count how many paths per tag
tag_counts = {entry["tag"]: len(entry.get("paths", [])) for entry in files}

# Filter & sort tags
filtered_tags = sorted(tag for tag in tag_counts if query in tag.lower()) if query else sorted(tag_counts)

# Build Alfred results
items = []
for tag in filtered_tags:
    count = tag_counts[tag]
    items.append({
        "title": tag,
        "subtitle": f"{count} file{'s' if count != 1 else ''} • ↵ view • ⌘ remove • ⌥ rename • ⌃ tag • ⇧ view all",
        "arg": tag,
        "mods": {
            "cmd": {
                "arg": tag,
                "subtitle": f"⌘↵ to remove tag: {tag}"
            },
            "alt": {
                "arg": tag,
                "subtitle": f"⌥↵ to rename tag: {tag}",
                "variables": {
                    "old_tag": tag
                }
            },
            "ctrl": {
                "arg": tag,
                "subtitle": f"⌃↵ to tag selected file(s) with: {tag}"
            },
            "shift": {
                "arg": tag,
                "subtitle": f"⇧↵ to open all files with: {tag}"
            }

        }
    })

# Output to Alfred
print(json.dumps({"items": items}))
