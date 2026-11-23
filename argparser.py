import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        prog="sh",
        description="Command language interpreter",
        allow_abbrev=False,
    )

    # Shell options
    parser.add_argument("-a", action="store_true")
    parser.add_argument("-b", action="store_true")
    parser.add_argument("-C", action="store_true")
    parser.add_argument("-e", action="store_true")
    parser.add_argument("-f", action="store_true")
    parser.add_argument("-i", action="store_true", help="Forces interactive behavior if the heuristic doesn't line up")
    parser.add_argument("-m", action="store_true")
    parser.add_argument("-n", action="store_true")
    parser.add_argument("-u", action="store_true")
    parser.add_argument("-v", action="store_true")
    parser.add_argument("-x", action="store_true")

    # Invocation modes
    modes = parser.add_mutually_exclusive_group()

    modes.add_argument(
        "-c",
        metavar="COMMAND",
        dest="command",
    )

    modes.add_argument(
        "-s",
        action="store_true",
    )

    parser.add_argument(
        "COMMAND_FILE",
        nargs="?",
        default=None
    )

    # Remaining positional arguments
    parser.add_argument(
        "arguments",
        nargs="*",
    )

    return parser

def normalize_options(argv):
    normalized = []
    shell_options = {}

    for arg in argv:
        if arg.startswith(("-", "+")) and len(arg) > 1:
            enabled = arg[0] == "-"

            if arg[1] in "abCefimnuvx":
                for option in arg[1:]:
                    shell_options[option] = enabled
                continue

        normalized.append(arg)

    return normalized, shell_options

def _parse_args(argv):
    parser = create_parser()
    return parser.parse_args(argv)

def parse_args(argv):
    argv, shell_options = normalize_options(argv[1:])
    args = _parse_args(argv)
    return args