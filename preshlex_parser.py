import os
import re

_VARIABLE = re.compile(
    r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))"
)
_ESCAPE = re.compile(
    r"\\[A-Za-z0-9\*\'\"]"
)

escapes={
    r'\"': '"', # double quote
    r"\'": "'", # single quote
    r"\\": "\\", # backslash
    r"\a": "\a", # alert character
    r"\b": "\b", # backspace character (legacy: please hit the actual key to fix your mistakes, it's right there!)
    r"\e": "\x1b", # escape character (legacy on desktop: XOrg a typically handles this)
    r"\f": "\f", # form feed character
    r"\n": "\n", # newline character
    r"\r": "\r", # carriage return (SHOULD BE LEGACY: THIS IS A COMPUTER NOT A TYPEWRITER, MICROSLOP!)
    r"\t": "\t", # tab
    r"\v": "\v" # vertical tab (legacy: who types this anymore?)
}

def _parse(command):
    def substitute(match):
        variable = match.group(1) or match.group(2)
        return os.environ.get(variable, match.group(0))

    return _VARIABLE.sub(substitute, command)

def substitute_escapes(command):
    def substitute(match):
        variable = match.group(1) or match.group(2)
        return escapes[variable]

    return _VARIABLE.sub(substitute, command)

def strip_comments(command):
    result = []
    quote = None
    escaped = False

    for char in command:
        if escaped:
            result.append(char)
            escaped = False
            continue

        if char == "\\" and quote != "'":
            result.append(char)
            escaped = True
            continue

        if quote:
            if char == quote:
                quote = None
            result.append(char)
            continue

        if char in ("'", '"'):
            quote = char
            result.append(char)
            continue

        if char == "#":
            break

        result.append(char)

    return "".join(result)

def parse(command):
    return _parse(strip_comments(command))