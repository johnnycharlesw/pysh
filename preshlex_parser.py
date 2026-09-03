import os
import re

_VARIABLE = re.compile(
    r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))"
)

def parse(command):
    def substitute(match):
        variable = match.group(1) or match.group(2)
        return os.environ.get(variable, match.group(0))

    return _VARIABLE.sub(substitute, command)
