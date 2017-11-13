# TODO:
#  - handle tab and other non-monospace characters better
#  - recognize numeric columns and right justify them

from collections import defaultdict
from itertools import zip_longest
from operator import itemgetter
from statistics import median_low


def _squeeze(lines, width):
    """
    Squeeze the contents of a cell into a fixed width column, breaking lines on spaces where possible.

    :param lines: list of string lines in the cell
    :param width: fixed width of the column
    :return: list of lines squeezed to fit
    """
    if all(len(line) <= width for line in lines):
        return lines
    out = []
    token_lines = [line.split(" ") for line in lines]
    for token_line in token_lines:
        line = []
        for token in token_line:
            if sum(len(token) for token in line) + len(token) + len(line) > width:
                if line:
                    out.append(" ".join(line))
                while len(token) > width:
                    out.append(token[:width])
                    token = token[width:]
                line = [token]
            else:
                line.append(token)
        out.append(" ".join(line))
    return out


def fmt(fmt_str):
    """
    Helper to convert a format string into a function that allies its argument to the format.

    :param fmt_str: string appropriate for using with string.format
    :return: A function which applies its single argument to fmt_str
    """
    return lambda item: fmt_str.format(item)


def ljust(s, width):
    return s.ljust(width)


def rjust(s, width):
    return s.rjust(width)


def cjust(s, width):
    if width <= len(s):
        return s
    extra = width - len(s)
    r = extra // 2
    l = r + extra % 2
    s = s.ljust(l + len(s))
    return s.rjust(r + len(s))


def ptable(headers, *rows, max_width=200, str=str, str_by_type={}, justification=()):
    """
    Make an easily readable table.

    :param headers: iterable of header values
    :param rows: iterables of column contents (must all be the same length as headers)
    :param max_width: maximum number of columns for the table (including margins and separators)
    :param str: function to convert items to strings
    :param str_by_type: dictionary mapping types to custom str functions to be used for those types
                        used in preference over default str except for headers which always use default str
    :return: a string containing the table
    """
    headers = [str(h).split("\n") for h in headers]
    rows = [[(str_by_type.get(type(c)) or str)(c).split("\n") for c in row] for row in rows]
    assert len(set(len(row) for row in rows) | {len(headers)}) == 1, "headers and rows must have same number of columns"
    # 2 chars padding on the left, 3 between each column, 2 on the right
    available_width = max_width - 2 - (len(headers) - 1) * 3 - 2
    assert available_width >= len(headers), "must provide enough width for at least one character per column"
    # use the max and median widths of each column to see if any need to be squeezed to fit the overall max_width
    col_width_maxes = []
    col_width_medians = []
    # zip(*rows) transposes to columns
    # zip_longest in case there are no rows
    for header, col in zip_longest(headers, zip(*rows), fillvalue=()):
        widths = [max(len(line) for line in r) for r in col]
        widths.append(max(len(line) for line in header))
        col_width_maxes.append(max(widths))
        col_width_medians.append(median_low(widths))
    col_widths = col_width_maxes

    if sum(col_width_maxes) > available_width:
        # reduce the column with the greatest difference between max and median width by one repeatedly until it fits
        diffs = {i: d for i, d in enumerate(mx - md for mx, md in zip(col_width_maxes, col_width_medians))}
        to_chop = defaultdict(int)
        while sum(col_width_maxes) - sum(to_chop.values()) > available_width:
            i, _ = max(diffs.items(), key=itemgetter(1))
            diffs[i] -= 1
            to_chop[i] += 1
        for i, tc in to_chop.items():
            col_widths[i] -= tc
        headers = [_squeeze(h, col_widths[i]) for i, h in enumerate(headers)]
        rows = [[_squeeze(c, col_widths[i]) for i, c in enumerate(row)] for row in rows]
        # recalculate the max width after the squeeze and use the lesser of that and the current width to avoid
        # whitespace at the end of wrapped lines
        for i, (header, col) in enumerate(zip_longest(headers, zip(*rows), fillvalue=())):
            widths = [max(len(line) for line in r) for r in col]
            widths.append(max(len(line) for line in header))
            col_widths[i] = min(col_widths[i], max(widths))

    out = ""
    header_height = max(len(h) for h in headers)
    for header in headers:
        header.extend([""] * (header_height - len(header)))
    for line in zip(*headers):
        out += "| {} |\n".format(
            " | ".join(
                just(col_line, col_widths[i])
                for i, (just, col_line)
                in enumerate(zip_longest(justification, line, fillvalue=ljust))))
    out += "|"
    for just, cw in zip_longest(justification, col_widths, fillvalue=ljust):
        # markdown justification markers
        l = ":" if just in (ljust, cjust) else " "
        r = ":" if just in (cjust, rjust) else " "
        out += "{}{}{}|".format(l, "-" * cw, r)
    out += "\n"
    for row in rows:
        row_height = max(len(c) for c in row)
        for col in row:
            col.extend([""] * (row_height - len(col)))
        for line in zip(*row):
            out += "| {} |\n".format(
                " | ".join(
                    just(col_line, col_widths[i])
                    for i, (just, col_line)
                    in enumerate(zip_longest(justification, line, fillvalue=ljust))))
    return out
