import os
import sys
history = []
def rp_input(prompt):
    current_index=len(history)
    print(prompt, end="", flush=True)
    unfinished = True
    cursor = 0
    buffer = []

    def redraw():
        print("\r" + prompt  + "".join(buffer) + "\033[K", end="", flush=True)

        offset = len(buffer) - cursor
        if offset > 0:
            print(f"\033[{offset}D", end="", flush=True)

    
    def get_key():
        if os.name=="nt":
            import msvcrt
            key = msvcrt.getwch()
            if key in ("\x00", "\xe0"):
                key = msvcrt.getwch()
                return {
                    "H": "UP",
                    "P": "DOWN",
                    "K": "LEFT",
                    "M": "RIGHT",
                    "S": "DELETE"
                }.get(key, "UNKNOWN")
            return key
        elif os.name=="posix":
            import tty
            import termios
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)

            try:
                tty.setcbreak(fd)
                key = sys.stdin.read(1)

                if key == "\x1b":
                    key += sys.stdin.read(1)

                    if key == "\x1b[":
                        key += sys.stdin.read(1)

                    return {
                        "\x1b[A": "UP",
                        "\x1b[B": "DOWN",
                        "\x1b[C": "RIGHT",
                        "\x1b[D": "LEFT",
                    }.get(key, "UNKNOWN")

                return key
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        else:
            stdin = sys.stdin
            key = stdin.read(1)
            print(key, end="", sep="")
            return key
    
    while unfinished:
        key = get_key()

        if key == "\r" or key == "\n":
            unfinished = False
            print()
        elif key == "\x03":
            raise KeyboardInterrupt
        elif key == "\x04":
            if not buffer:
                raise EOFError
        elif key == "LEFT":
            if cursor > 0:
                cursor -= 1
                print("\033[1D", end="", flush=True)
        elif key == "RIGHT":
            if cursor < len(buffer):
                cursor += 1
                print("\033[1C", end="", flush=True)
        elif key == "UP":
            if current_index > 0:
                current_index -= 1
                buffer = list(history[current_index])
                cursor = len(buffer)
                redraw()

        elif key == "DOWN":
            if current_index < len(history):
                current_index += 1

                if current_index == len(history):
                    buffer = []
                else:
                    buffer = list(history[current_index])

                cursor = len(buffer)
                redraw()
                
        elif key in ("\x7f", "\b"):
            if cursor > 0:
                cursor -= 1
                buffer.pop(cursor)

                redraw()
                offset = len(buffer) + 1 - cursor
                print(f"\033[{offset}D", end="", flush=True)
        elif isinstance(key, str) and len(key) == 1 and key.isprintable():
            buffer.insert(cursor, key)

            print("".join(buffer[cursor:]), end="", flush=True)

            cursor += 1

            remaining = len(buffer) - cursor
            if remaining:
                print(f"\033[{remaining}D", end="", flush=True)
    out = "".join(buffer)
    if out.strip():
        history.append(out)
        current_index+=1
    return out