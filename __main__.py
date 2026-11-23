#!/bin/python3
import shlex
import subprocess
import os, sys
import promptgen
import messages
import pysh_builtins
import getpass
import argparser
from execution import execute_posix, execute_python, execute_script, run_command
exitcode = 0
displayexitcodes = False
priviliged_users = promptgen.priviliged_users

show_prompt = True

def display_message(islogin):
    if not islogin:
        return
    if getpass.getuser() in priviliged_users:
        print("""
        Warning: this terminal is running as the superuser.
        EagletOS comes with absolutely no warranty whatsoever, so if you mess up something, the EagletOS developers are not responsible.
        """)
    else:
        print("""
        This terminal is not running as the superuser, but just a reminder, not every command needs to be prefixed with `sudo` or `pkexec`.
        """)

def run_startup_scripts(home, islogin):
    # If this is a login shell, load the "profile" scripts, otherwise the "pyshrc" scripts
    scripts = []

    script_type="pyshrc"

    if islogin:
        script_type="profile"
    else:
        show_prompt = False 

    scripts.append(os.path.join("/", "etc", script_type))
    scripts.append(os.path.join(home, f".{script_type}"))
    scripts.append(os.path.join(home, f".pysh_{script_type}"))

    for script in scripts:
        if os.path.isfile(script):
            execute_script(script)

def read_prompt():
    prompt = None
    if show_prompt:
        prompt = promptgen.promptgen()
    else:
        prompt = ""
    command = input(prompt)
    return command

def get_is_interactive(args):
    flag = args.i
    is_graphical = "DISPLAY" in os.environ.keys()
    is_interpreter = (
        args.command is not None
        or args.s
        or args.COMMAND_FILE is not None
    )
    return flag or (is_graphical and not is_interpreter)

def main():
    args = argparser.parse_args(sys.argv)
    run_startup_scripts(
        pysh_builtins.home, # home directory
        get_is_interactive(args) # graphical command prompts count as login shells here (weird, right?)
    )

    display_message(get_is_interactive(args))

    if (not get_is_interactive(args)) and args.COMMAND_FILE is not None:
        execute_script(args.COMMAND_FILE)
        return

    while True:
        try:
            # Recieve command
            command = read_prompt()
            # Check for the `exit` command
            if command == "":
                continue # Don't mind blank lines
            elif command.startswith("abracadabra"):
                print("Does this look like magic to you?")
                continue
            elif command.endswith("make me a sandwich"):
                print("Maybe you didn't mean to trigger GNU Make, but I guess it will get compiled anyways.")
            # elif command.endswith("rm -rf C:"):
            #     print("No, EagletOS does not have drive letters, it is based on Debian.")
            #     continue
            elif command.split(" ")[0] == "alias":
                exitcode = pysh_builtins.alias(command)
                continue

            # Run command
            run_command(command)

            # Display exit code
            if displayexitcodes:
                print(f"Command `{command}` exited with code {exitcode}")
        except KeyboardInterrupt:
            print("Keyboard interrupt!")
            continue

if __name__ == "__main__":
    main()