import os

def get_bookmark_icon():
    browser = os.environ.get("browser", "Safari")
    paths = {
        "Safari": "/System/Applications/Safari.app",
        "Google Chrome": "/Applications/Google Chrome.app",
        "Brave Browser": "/Applications/Brave Browser.app",
        "Microsoft Edge": "/Applications/Microsoft Edge.app",
        "Arc": "/Applications/Arc.app"
    }

    icon_path = paths.get(browser, "icons/bookmark.png")
    icon = { "path": icon_path }
    if icon_path.endswith(".app"):
        icon["type"] = "fileicon"
    return icon
