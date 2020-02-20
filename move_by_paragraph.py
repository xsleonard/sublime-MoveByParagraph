from __future__ import print_function
from sublime import Region, load_settings
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

    def run(self,
            edit,
            extend=False,
            forward=False,
            ignore_blank_lines=True,
            stop_at_paragraph_begin=True,
            stop_at_paragraph_end=False):
        """
        The cursor will move to beginning of a non-empty line that succeeds
        an empty one.  Selection is supported when "extend" is True.
        """
        if not stop_at_paragraph_begin and not stop_at_paragraph_end:
            print('[WARNING] MoveByParagraph: stop_at_paragraph_begin and '
                  'stop_at_paragraph_end are both False, nothing will happen')
            return

        cursor = self.get_cursor()
        if cursor.a < cursor.b:
            start = cursor.end()
        else:
            start = cursor.begin()

        kwargs = dict(ignore_blank_lines=ignore_blank_lines,
                      stop_at_paragraph_begin=stop_at_paragraph_begin,
                      stop_at_paragraph_end=stop_at_paragraph_end)

        dbg('Starting from', cursor)

        if forward:
            next_cursor = self._find_paragraph_position_forward(start,
                                                                **kwargs)
        else:
            next_cursor = self._find_paragraph_position_backward(start,
                                                                 **kwargs)

        dbg('Stopping at', next_cursor)

        if extend:
            dbg('set_selection_to', cursor.a, next_cursor.begin())
            self.set_selection_to(cursor.a, next_cursor.begin())
        else:
            dbg('set_cursor_to', next_cursor.begin())
            self.set_cursor_to(next_cursor.begin())

        cursor = self.get_cursor()
        self.view.show(cursor)

    def _find_paragraph_position_forward(self,
                                         start,
                                         ignore_blank_lines=True,
                                         stop_at_paragraph_begin=True,
                                         stop_at_paragraph_end=False):
        size = self.view.size()
        r = Region(start, size)

        # Obtain the lines that intersect the region
        lines = self.view.lines(r)

        for n, line in enumerate(lines[:-1]):
            if (stop_at_paragraph_begin and
                self._line_begins_paragraph(lines[n+1],
                                            line,
                                            ignore_blank_lines)):
                return Region(lines[n+1].a, lines[n+1].a)

            if (line.b != start and
                stop_at_paragraph_end and
                self._line_ends_paragraph(line,
                                          lines[n+1],
                                          ignore_blank_lines)):
                return Region(line.b, line.b)

        # Check if the last line is empty or not
        # If it is empty, make sure we jump to the end of the file
        # If it is not empty, jump to the end of the line
        if self._substr(lines[-1], ignore_blank_lines) == '':
            return Region(size, size)

        end = lines[-1].b

        # If the file ends with a single newline, it will be stuck
        # before this newline character unless we do this
        if end == start:
            return Region(end+1, end+1)

        return Region(end, end)

    def _find_paragraph_position_backward(self,
                                          start,
                                          ignore_blank_lines=True,
                                          stop_at_paragraph_begin=True,
                                          stop_at_paragraph_end=False):
        r = Region(0, start)

        # Obtain the lines that intersect the region
        lines = self.view.lines(r)
        lines.reverse()

        for n, line in enumerate(lines[:-1]):
            if (stop_at_paragraph_begin and
                self._line_begins_paragraph(line,
                                            lines[n+1],
                                            ignore_blank_lines)):
                return Region(line.a, line.a)

            if (stop_at_paragraph_end and
                self._line_ends_paragraph(lines[n+1],
                                          line,
                                          ignore_blank_lines)):
                return Region(lines[n+1].b, lines[n+1].b)

        return lines[-1]

    def _line_begins_paragraph(self, line, line_above, ignore_blank_lines):
        a = self._substr(line, ignore_blank_lines)
        b = self._substr(line_above, ignore_blank_lines)
        dbg('line_above', line_above, self.view.substr(line_above))
        dbg('line', line, self.view.substr(line))
        return a and not b

    def _line_ends_paragraph(self, line, line_below, ignore_blank_lines):
        a = self._substr(line, ignore_blank_lines)
        dbg('line', line, self.view.substr(line))
        dbg('line_below', line_below, self.view.substr(line_below))
        b = self._substr(line_below, ignore_blank_lines)
        return a and not b

    def _substr(self, line, ignore_blank_lines):
        s = self.view.substr(line)
        if ignore_blank_lines:
            return s.strip()
        return s
