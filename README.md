sublime-MoveBetter
==================

A Sublime Text 2 plugin extension to the move command

A new command is added, `"move_better"`.  This extends the `"args"` of the built-in 
`"move"` command with additional functionality.


Moving by Paragraph
===================

Example (add this to your keymap):

    {"keys": ["ctrl+up"], "command": "move_better", "args": {"by": "paragraph", "forward": false}}
    {"keys": ["ctrl+down"], "command": "move_better", "args": {"by": "paragraph", "forward": true}}

![Paragraph Movement](http://i.imgur.com/E4VlmZO.gif)

Example with selection (add this to your keymap):

     {"keys": ["ctrl+shift+up"], "command": "move_better", "args": {"by": "paragraph", "forward": false, "extend": true}}
     {"keys": ["ctrl+shift+down"], "command": "move_better", "args": {"by": "paragraph", "forward": true, "extend": true}}

![Paragraph Selection](http://i.imgur.com/rXK3bcS.gif)
