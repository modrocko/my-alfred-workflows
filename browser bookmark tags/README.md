# Browser Bookmark Tags

Tag browser tabs with a label. Way easier than doing with your browser.

Part of a complete tagging system:  [Apple Mail Tags](https://github.com/modrocko/apple-mail-tags-alfred-workflow) | [Browser Bookmark Tags](https://github.com/modrocko/browser-bookmark-tags-alfred-workflow) | [Finder File Tags](https://github.com/modrocko/finder-file-tags-alfred-workflow) | [To-Do Task Tags](https://github.com/modrocko/todo-task-tags-alfred-workflow)

▸  Requires [jq](https://formulae.brew.sh/formula/jq)

## Usage

Here're the main functions for for this workflow (*does not support Firefox — yet*)

*💡 **Tip**: Type '!' to mark & save tags as '❗' (high priority)*  

### Initialize workflow

❗Type `:bt init` to run this operation to start using this workflow

![](assets/init.png)      

<kbd>↵</kbd> Initialize the workflow

<kbd>⌘</kbd> <kbd>↵</kbd> Reset data files *(will delete current data files & recreate new ones)* 

### Select your browser

❗Select one of the supported browsers in the `Configure Workflow` to use this workflow.

### Show all Browser Bookmark Tag options

Type `bt` to view top level functions

![](assets/start.png)  

### Assign a tag

Type `bta` to view all tags *(defaults or previously specified tags)*

Select or type a new label to tag the front-most browser tab

![](assets/assign.png)  

<kbd>↵</kbd> Tag front-most browser tab

### List tagged browser tabs

Type `btl` to view a list of all items grouped by tag

![](assets/btl.png)  

<kbd>↵</kbd>  View all browser tabs for selected tag

<kbd>⌘</kbd> <kbd>↵</kbd> Remove selected tag from all tagged tabs

<kbd>⌥</kbd> <kbd>↵</kbd> Rename selected tag for all tabs

<kbd>⌃</kbd> <kbd>↵</kbd> Tag front-most tab for selected tag

<kbd>⇧</kbd> <kbd>↵</kbd> Open all tabs for the selected tag

### Search tagged browser tabs

Type `bts` to search through all tagged webpages

![image-20250418145842968](assets/bts.png) 

<kbd>↵</kbd>  View file for selected item

<kbd>⌘</kbd> <kbd>↵</kbd> Remove tag from selected file

<kbd>⌥</kbd> <kbd>↵</kbd> Open the file and remove tag afterwards

<kbd>⌃</kbd> <kbd>↵</kbd> Reassign tag for selected file

### Apple Mail Tag Utilities

Type `:bt edit` to edit data files (if needed) and open underlying folders

![](assets/utils.png)    

<kbd>↵</kbd>  Open bookmarks file for manual edits via TextEdit.app

<kbd>⌘</kbd> <kbd>↵</kbd> Open default tags file for manual edit via TextEdit.app

<kbd>⌥</kbd> <kbd>↵</kbd> Open the data folder for this workflow

<kbd>⌃</kbd> <kbd>↵</kbd> Open the workflow folder for this workflow
