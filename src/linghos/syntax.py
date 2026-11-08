"""Small helpers for safely scanning LINGHOS brace-delimited blocks."""

import re
from typing import List, Optional

_QUOTED_STRING = re.compile(r"""'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*'""")


def find_block_end(lines: List[str], start_index: int) -> Optional[int]:
    """Return the matching closing-brace line for a block, or None if unclosed.

    Comments and quoted strings are ignored so braces in either do not affect
    nesting. The opening brace may appear anywhere on the starting line.
    """
    depth = 0
    opened = False

    for index in range(start_index, len(lines)):
        code = _QUOTED_STRING.sub("", lines[index])
        code = code.split("//", 1)[0]

        opening = code.count("{")
        closing = code.count("}")
        if opening:
            opened = True
        depth += opening - closing

        if depth < 0:
            return None
        if opened and depth == 0:
            return index

    return None
