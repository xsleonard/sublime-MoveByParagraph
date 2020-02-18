# sublime-MoveByParagraph

A Sublime Text 2 plugin extension to the move command

A new command is added, `"move_by_paragraph"`.  These `"args"` are accepted:

- `"forward"` (bool): True if this moves down the page
- `"extend"` (bool): True if this should create a selection
- `ignore_blank_lines` (bool): Set to true to ignore lines with nothing but whitespace (excluding newline) as text for paragraph boundaries. Defaults to true.
- `stop_at_paragraph_begin` (bool): Set to true to stop the cursor at the beginning of paragraphs. Defaults to true
- `stop_at_paragraph_end` (bool): Set to true to stop the cursor at the end of paragraphs. Defaults to false. Both `stop_at_paragraph_begin` and `stop_at_paragraph_end` can be set at the same time.

## Moving by Paragraph

Example (add this to your keymap):

    {"keys": ["ctrl+up"], "command": "move_by_paragraph", "args": {"forward": false}},
    {"keys": ["ctrl+down"], "command": "move_by_paragraph", "args": {"forward": true}},

![Paragraph Movement](http://i.imgur.com/E4VlmZO.gif)

Example with selection (add this to your keymap):

     {"keys": ["ctrl+shift+up"], "command": "move_by_paragraph", "args": {"forward": false, "extend": true}},
     {"keys": ["ctrl+shift+down"], "command": "move_by_paragraph", "args": {"forward": true, "extend": true}},

![Paragraph Selection](http://i.imgur.com/rXK3bcS.gif)

Note that `"ctrl+shift+up/down"` will overwrite the default action of moving
the current selection up or down, which is why this is not set by default.
Personally, I remapped that behaviour to `"ctrl+t"` and `"ctrl+g"`.

## Suggested Plugins

- [Copy Block](https://sublime.wbond.net/packages/Copy%20Block)


