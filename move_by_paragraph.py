from __future__ import print_function
from sublime import Region
from sublime_plugin import TextCommand
from collections import Iterable


DEBUG = False


def dbg(msg):
    if DEBUG:
        print(msg)


class MyCommand(TextCommand):

    def set_cursor_to(self, pos):
        """ Sets the cursor to a given position. If multiple
        positions are given, a multicursor will be made.
        """
        dbg('setting cursor to {0}'.format(pos))
        if not isinstance(pos, Iterable):
            pos = [pos]
        self.view.sel().clear()
        for p in pos:
            self.view.sel().add(Region(p, p))

    def set_selection_to(self, start, end):
        dbg("setting selection to {0}".format((start, end)))
        self.view.sel().clear()
        self.view.sel().add(Region(start, end))

    def get_char_at(self, pos):
        """ Return the character at a position """
        return self.view.substr(Region(pos, pos + 1))

    def get_current_line(self):
        """ Return the line at the current cursor """
        return self.get_line_at(self.get_cursor())

    def get_line_at(self, region):
        """ Returns the :class:`sublime.Line` at a
        :class:`sublime.Region`
        """
        return self.view.line(region)

    def get_cursor(self):
        """ Returns the first current cursor """
        return self.view.sel()[0]


class MoveByParagraphCommand(MyCommand):
    def run(self, edit, extend=False, forward=False):
        """
        The cursor will move to beginning of a non-empty line that succeeds
        an empty one.  Selection is supported when "extend" is True.
        """
        cursor = self.get_cursor()
        self.move_args = {"by": "stops", "forward": forward,
                          "empty_line": True, "extend": extend}
        self.view.run_command('move', self.move_args)
        self.set_paragraph_cursor(cursor, extend=extend, forward=forward)

    def set_paragraph_cursor(self, cursor, extend=False, forward=False):
        """ Readjusts the final cursor placement after navigating by
        "stops" to a "paragraph" based position.
        """
        currcursor = cursor.begin()
        if extend and forward:
            currcursor = cursor.end()
        currline = self.get_line_at(currcursor)
        s = self.get_cursor()
        if forward:
            pos = s.end()
        else:
            pos = s.begin()
        size = self.view.size()

        if forward:
            while self.get_char_at(pos) == '\n' and pos < size:
                pos += 1
        else:
            if (currline > self.get_line_at(pos + 1) and pos and
                    self.get_char_at(pos + 1) != '\n'):
                # If we are jumping from underneath a spot we should stop
                pos += 1
            else:
                # If we are jumping from a stopline or higher, skim past all
                # upper newlines and into the next true block
                while self.get_char_at(pos) == '\n' and pos > 0:
                    pos -= 1
                # We reached the end of the upper block, move past that
                # line's newline and back into the highest level newline
                if pos:
                    pos += 2
                    if extend:
                        self.set_selection_to(cursor.end(), pos)
                    else:
                        self.set_cursor_to(pos)
                    self.view.run_command("move", self.move_args)
                    pos = self.get_cursor().begin()
                    if pos:
                        pos += 1

        if extend:
            # Doing a block selection
            if forward:
                # Moving down the page,
                # Start at where the initial cursor was
                start = cursor.begin()
                # End at where we calculated our paragraph cursor to be, but
                # we don't want to select all the way to the next paragraph
                end = pos
                if end != size:
                    end -= 1
            else:
                # Moving up the page,
                # Start at where we calculated our paragraph cursor to be
                start = pos
                if start:
                    pos -= 1
                # End at where our initial cursor was
                end = cursor.end()
                # Flip the selection so the cursor appears at the correct side
                start, end = end, start
            self.set_selection_to(start, end)
        else:
            self.set_cursor_to(max(0, min(size, pos)))
