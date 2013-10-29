sublime-MoveByParagraph
==================

A Sublime Text 2 plugin extension to the move command

A new command is added, `"move_by_paragraph"`.  Two `"args"` are accepted:

- `"forward"` (bool): True if this moves down the page
- `"extend"` (bool): True if this should create a selection


Moving by Paragraph
===================

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


Suggested Plugins
==================

- [Copy Block](https://sublime.wbond.net/packages/Copy%20Block)
