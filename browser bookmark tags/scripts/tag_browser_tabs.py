import os
import sys
import json
import subprocess

# Get tag
tag = sys.argv[1].strip().replace("!", "❗")

# Resolve paths
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "bookmarks.json")
notif_title = os.environ["alfred_workflow_name"]
browser = os.environ["browser"]

# Check if tagging all tabs or all windows
tag_all_tabs = os.getenv("tag_all_tabs", "") == "1"
tag_all_windows = os.getenv("tag_all_windows", "") == "1"

# AppleScript to get tabs info
if tag_all_windows:
    script = f'''
    tell application "{browser}"
        if it is running and (count of windows) > 0 then
            set output to ""
            repeat with w in windows
                repeat with t in tabs of w
                    set tabTitle to title of t
                    set tabURL to URL of t
                    set output to output & tabTitle & "||" & tabURL & "%%"
                end repeat
            end repeat
            return output
        end if
    end tell
    '''
elif tag_all_tabs:
    script = f'''
    tell application "{browser}"
        if it is running and (count of windows) > 0 then
            set output to ""
            repeat with t in tabs of front window
                set tabTitle to title of t
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
            set tabTitle to title of active tab of front window
            set tabURL to URL of active tab of front window
            return tabTitle & "||" & tabURL & "%%"
        end if
    end tell
    '''


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

# Ensure folder exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Load existing bookmarks
bookmarks = []
if os.path.exists(db_path):
    with open(db_path, "r") as f:
        bookmarks = json.load(f)

# Process each tab
added = 0
for item in decoded.split("%%"):
    if not item.strip():
        continue
    title, url = item.strip().split("||")
    exists = any(b["url"] == url and tag in b.get("tags", []) for b in bookmarks)

    if not exists:
        bookmarks.append({
            "title": title.strip(),
            "url": url.strip(),
            "tags": [tag]
        })
        added += 1

# Save bookmarks
with open(db_path, "w") as f:
    json.dump(bookmarks, f, indent=2)

# Notify
notif_text = f"Tagged {added} tab{'s' if added != 1 else ''} with '{tag}'"
subprocess.run([
    "osascript", "-e",
    f'display notification "{notif_text}" with title "{notif_title}"'
])

print(f"✅ {notif_text}")
