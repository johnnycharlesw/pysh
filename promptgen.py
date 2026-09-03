import os, sys
import socket
import getpass

prompt = ""
username = getpass.getuser()

def promptgen():
    # Get the prompt ending character

    promptend = "$"
    if username == "root" or username == "SYSTEM":
        promptend = "#"

    # Get the current working directory

    cwd = os.getcwd()

    # Get the current hostname

    hostname = socket.gethostname()

    # Generate the prompt

    formatted_username = f"\033[0;32m{username}@{hostname}\033[0m"
    formatted_cwd = f"\033[0;34m{cwd}\033[0m"
    prompt = f"{formatted_username}:{formatted_cwd}{promptend} "
    return prompt