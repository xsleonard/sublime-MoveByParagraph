from __future__ import print_function
from sublime import Region
from sublime_plugin import TextCommand
from collections import Iterable


DEBUG = False


def dbg(*msg):
    if DEBUG:
        print(' '.join(map(str, msg)))


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

    def _find_paragraph_position_forward(self, start):
        size = self.view.size()
        r = Region(start, size)
        lines = self.view.split_by_newlines(r)
        found_empty = False
        stop_line = None
        for n, line in enumerate(lines):
            s = self.view.substr(line)
            if (not s and self.view.substr(max(0, line.begin() - 1)) == '\n'
                    and n):
                found_empty = True
            elif found_empty:
                stop_line = line
                break
        if stop_line is None:
            if self.view.substr(Region(size - 1, size)) == '\n':
                # We want to jump to the very end if we reached the file and
                # it ends with a newline.  If the file ends with a newline,
                # the lines array does not end with u'' as expected, which is
                # why we need to do this
                stop_line = Region(size, size)
            else:
                stop_line = lines[-1]
        return stop_line

    def _find_paragraph_position_backward(self, start):
        r = Region(0, start)
        lines = self.view.split_by_newlines(r)
        lines.reverse()
        last_line = None
        last_str = u''
        stop_line = None
        for line in lines:
            s = self.view.substr(line)
            if (not s and last_str and last_line is not None and
                    lines[0] != last_line):
                stop_line = last_line
                break
            last_line = line
            last_str = s
        if stop_line is None:
            stop_line = lines[-1]
        return stop_line

    def find_paragraph_position(self, start, forward=False):
        dbg('Starting from {0}'.format(start))
        if forward:
            return self._find_paragraph_position_forward(start)
        else:
            return self._find_paragraph_position_backward(start)

    def run(self, edit, extend=False, forward=False):
        """
        The cursor will move to beginning of a non-empty line that succeeds
        an empty one.  Selection is supported when "extend" is True.
        """
        cursor = self.get_cursor()
        if cursor.a < cursor.b:
            start = cursor.end()
        else:
            start = cursor.begin()
        line = self.find_paragraph_position(start, forward=forward)
        dbg('Stopping at {0}'.format(self.view.substr(line)))

        if extend:
            self.set_selection_to(cursor.a, line.begin())
        else:
            self.set_cursor_to(line.begin())
        cursor = self.get_cursor()
        self.view.show(cursor)
