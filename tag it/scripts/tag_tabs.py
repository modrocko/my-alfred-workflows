import os
import sys
import json
import subprocess
import uuid

# Get tag
tag = sys.argv[1].strip().replace("!", "❗")
if not tag:
    sys.exit(0)

# Paths & setup
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
notif_title = os.environ["alfred_workflow_name"]
browser = os.environ.get("browser", "Safari")

print("browser:", browser, file=sys.stderr)

tag_scope = os.environ.get("tag_scope", "single_tab")

# decide which AppleScript property to use
title_prop = "name" if browser == "Safari" else "title"

# then build each script using that prop
if tag_scope == "all_tabs_all_windows":
    script = f'''
    tell application "{browser}"
        if it is running and (count of windows) > 0 then
            set output to ""
            repeat with w in windows
                repeat with t in tabs of w
                    set tabTitle to {title_prop} of t
                    set tabURL to URL of t
                    set output to output & tabTitle & "||" & tabURL & "%%"
                end repeat
            end repeat
            return output
        end if
    end tell
    '''
elif tag_scope == "all_tabs_window":
    script = f'''
    tell application "{browser}"
        if it is running and (count of windows) > 0 then
            set output to ""
            repeat with t in tabs of front window
                set tabTitle to {title_prop} of t
                set tabURL to URL of t
                set output to output & tabTitle & "||" & tabURL & "%%"
            end repeat
            return output
        end if
    end tell
    '''
else:
    script = f'''
    tell application "{browser}"
        if it is running and (count of windows) > 0 then
            set tabTitle to {title_prop} of active tab of front window
            set tabURL to URL of active tab of front window
            return tabTitle & "||" & tabURL & "%%"
        end if
    end tell
    '''


## AppleScript to extract tab(s) info
#if tag_scope == "all_tabs_all_windows":
#    script = f'''
#    tell application "{browser}"
#        if it is running and (count of windows) > 0 then
#            set output to ""
#            repeat with w in windows
#                repeat with t in tabs of w
#                    set tabTitle to title of t
#                    set tabURL to URL of t
#                    set output to output & tabTitle & "||" & tabURL & "%%"
#                end repeat
#            end repeat
#            return output
#        end if
#    end tell
#    '''
#elif tag_scope == "all_tabs_window":
#    script = f'''
#    tell application "{browser}"
#        if it is running and (count of windows) > 0 then
#            set output to ""
#            repeat with t in tabs of front window
#                set tabTitle to title of t
#                set tabURL to URL of t
#                set output to output & tabTitle & "||" & tabURL & "%%"
#            end repeat
#            return output
#        end if
#    end tell
#    '''
#else:  # default to single
#    script = f'''
#    tell application "{browser}"
#        if it is running and (count of windows) > 0 then
#            set tabTitle to title of active tab of front window
#            set tabURL to URL of active tab of front window
#            return tabTitle & "||" & tabURL & "%%"
#        end if
#    end tell
#    '''

# Run AppleScript
try:
    result = subprocess.check_output(["osascript", "-e", script])
    decoded = result.decode("utf-8").strip()
    if not decoded:
        raise ValueError("No tab data returned")
except:
    subprocess.run([
        "osascript", "-e",
        f'display notification "No browser window found to tag." with title "{notif_title}"'
    ])
    sys.exit(1)

# Load or init items.json
if os.path.exists(items_path):
    with open(items_path, "r") as f:
        data = json.load(f)
else:
    data = []

# Find or create tag block
tag_block = next((b for b in data if b.get("tag") == tag), None)
if not tag_block:
    tag_block = { "tag": tag, "items": [] }
    data.append(tag_block)

# Process tabs into bookmark items
added = 0
for item in decoded.split("%%"):
    if not item.strip():
        continue
    parts = item.strip().split("||")
    if len(parts) != 2:
        continue

    title, url = parts[0].strip(), parts[1].strip()

    already_tagged = any(
        entry.get("type") == "bookmark" and entry.get("url") == url
        for entry in tag_block["items"]
    )

    if not already_tagged:
        tag_block["items"].append({
            "type": "bookmark",
            "title": title,
            "url": url,
            "uid": str(uuid.uuid4())
        })
        added += 1

# Save
with open(items_path, "w") as f:
    json.dump(data, f, indent=2)

# Notify
notif_text = f"Tagged {added} tab{'s' if added != 1 else ''} with '{tag}'"
subprocess.run([
    "osascript", "-e",
    f'display notification "{notif_text}" with title "{notif_title}"'
])

print(f"✅ {notif_text}")
