"""Lexical helpers shared by the LINGHOS compiler and interpreter."""

from typing import List, Optional


def strip_inline_comment(line: str) -> str:
    """Strip // comments without treating quoted URL-like text as a comment."""
    quote = None
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == "/" and index + 1 < len(line) and line[index + 1] == "/":
            return line[:index]
        index += 1
    return line


def normalize_script(source: str) -> str:
    """Normalize quotes and put structural delimiters on separate lines.

    Braces and semicolons inside quoted strings or comments are preserved.
    """
    source = (source.replace("’", "'").replace("‘", "'")
                    .replace("“", '"').replace("”", '"'))
    output = []
    quote = None
    escaped = False
    in_comment = False
    index = 0

    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""

        if in_comment:
            output.append(char)
            if char == "\n":
                in_comment = False
        elif quote:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
            output.append(char)
        elif char == "/" and next_char == "/":
            in_comment = True
            output.append("//")
            index += 1
        elif char in ("{", "}"):
            if output and not output[-1].endswith("\n"):
                output.append("\n")
            output.extend((char, "\n"))
        elif char == ";":
            output.extend((char, "\n"))
        else:
            output.append(char)
        index += 1

    return "".join(output)


def _mask_quoted_text(line: str) -> str:
    """Replace string contents with spaces while preserving character count."""
    output = list(line)
    quote = None
    escaped = False
    for index, char in enumerate(line):
        if quote:
            output[index] = " "
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
            output[index] = " "
    return "".join(output)


def find_block_end(lines: List[str], start_index: int) -> Optional[int]:
    """Find a matching closing-brace line, ignoring comments and strings.

    Returns None for a missing opening or closing brace, or malformed nesting.
    """
    depth = 0
    opened = False
    for index in range(start_index, len(lines)):
        code = _mask_quoted_text(strip_inline_comment(lines[index]))
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
