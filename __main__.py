#!/bin/python3
import preshlex_parser
import shlex
import subprocess
import os, sys
import promptgen
import messages
import pysh_builtins
prompt = ""
exitcode = 0

if os.getenv("USER") == "root":
    print("""
    Warning: this terminal is running as the superuser.
    EagletOS comes with absolutely no warranty whatsoever, so if you mess up something, the EagletOS developers are not responsible.
    """)
else:
    print("""
    This terminal is not running as root, but just a reminder, not every command needs to be prefixed with `sudo` or `pkexec`.
    """)

while True:
    try:
        prompt = promptgen.promptgen()
        # Recieve command
        command = input(prompt)
        command = preshlex_parser.parse(command)
        # Check for the `exit` command
        if command == "exit":
            pysh_builtins.exit_() # The exit command is needed to exit the shell
        elif command == "":
            continue # Don't mind blank lines
        elif command == "history | sh":
            print("Don't pipe the roman empire into sh-you might regret it.")
            continue
        elif command.split(" ")[0] == "dd":
            print("Don't even think about using the Data Destroyer. If you need to wipe an old SSD, ask your parent to do so.")
            continue
        elif command.startswith("rm -rf /") or command.startswith("sudo rm -rf /") or command.startswith("pkexec rm -rf /"):
            print("Do you think wiping the main disk is a good idea? If you were in fact not intending that, use a relative path.")
            continue
        elif command.startswith("abracadabra"):
            print("Does this look like magic to you?")
            continue
        elif command.endswith("make me a sandwich"):
            print("Maybe you didn't mean to trigger GNU Make, but I guess it will get compiled anyways.")
        elif command.endswith("rm -rf C:"):
            print("No, EagletOS does not have drive letters, it is based on Debian.")
            continue
        elif command.split(" ")[0] == "cd":
            exitcode = pysh_builtins.cd(command)
            continue
        elif command == "pwd":
            exitcode = pysh_builtins.pwd()
            continue
        elif command.split(" ")[0] == "alias":
            exitcode = pysh_builtins.alias(command)
            continue

        # Run command
        try:
            lexed = shlex.split(command)
            exitcode = subprocess.call(lexed)
        except FileNotFoundError:
            print(messages.command_not_found)
            exitcode = -1

        

        # Display exit code
        # print(f"Command `{command}` exited with code {exitcode}")
    except KeyboardInterrupt:
        print("Keyboard interrupt!")
        continue

