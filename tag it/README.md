# Tag It!

Tag emails, files, folders & web pages for easy access later on.

I created this workflow to keep related items together for certain activities — all in one place. Projects, research, orders, favorites, recipes... whatever. I mainly use this for short term stuff. Less so for long-term bookmarks. I can tag, find & open email, files, folders & webpages in a breeze. 

So, to summarize... a consolidated Alfred system to:  

✓  Keep your projects organized  
✓  Keep your work moving forward  
✓  Keep your brain sane

Works with: Apple Mail ∙ Apple Finder ∙ Chrome-based browsers

▸ Requires [jq](https://formulae.brew.sh/formula/jq)

## Usage

Easy — just press a bunch of the option keys to start saving, finding & viewing emails, files, folders & browser tabs. 

### Main workflows

![image-20250509211540846](assets/image-20250509211540846.png)  

### Initialize workflow

▸ In *Configure Workflow*: 1) Select browser preference ∙ 2) Select tagging preference for browser window(s)

▸ Initialize the workflow to create the underlying data file *(see below)*

![image-20250509205555344](assets/image-20250509205555344.png) 

<kbd>↵</kbd>  Initialize the workflow

<kbd>⌘</kbd><kbd>↵</kbd> Reset data files (destructive action, will delete all existing data)

### Tag something

Tag emails, files, folders or browser tabs. Keep typing to create a new tag. Or select an existing tag.

![image-20250516140908870](assets/image-20250516140908870.png)  

<kbd>↵</kbd>  Tag all selected emails in Apple Mail window

<kbd>⌘</kbd><kbd>↵</kbd> Tag all selected files in front-most Finder window

<kbd>⌥</kbd><kbd>↵</kbd> Tag all browser tabs as per preference setting

<kbd>⌃</kbd><kbd>↵</kbd> Tag all selected files in front-most Finder window - but mark them as type `note` ★

>  *★ I added this item type to tag files as a `note` to make it visually easy to see. Keep your project notes or tasks or whatever for any saved tag. Works great — you'll see.*

### Show tagged items

From the previous dialog... show all tags containing items for that tag.

![image-20250509221638765](assets/image-20250509221638765.png) 

<kbd>↵</kbd>  View list of item types for this tag (emails, files & tabs)

<kbd>⌘</kbd><kbd>↵</kbd> Rename this tag

<kbd>⌥</kbd><kbd>↵</kbd> Remove this tag & all its tagged items

<kbd>⌃</kbd><kbd>↵</kbd> View flat list all items for this tag

## Show item types

From the previous dialog... show tagged items, grouped by item type.

![image-20250511163058886](assets/image-20250511163058886.png) 

<kbd>↵</kbd>  View items for that item type

<kbd>⌘</kbd><kbd>↵</kbd>  Tag more items of that item type

<kbd>⌥</kbd><kbd>↵</kbd>  Remove items of that item type

<kbd>⌃</kbd><kbd>↵</kbd>  Open all items of that item type

### Search tagged items

Show complete, flat list of all previously tagged items. Start typing to filter the list by title, tag, & more fields.

 ![image-20250512152357689](assets/image-20250512152357689.png) 

<kbd>↵</kbd>  Open the selected item

<kbd>⌘</kbd><kbd>↵</kbd> Remove the item (untag) from this tag

<kbd>⌥</kbd><kbd>↵</kbd> Rename the item (good for applying a note too)

