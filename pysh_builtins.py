import os, sys
import time

def exit_():
    print("Bye!")
    time.sleep(1)
    exit(0)

def alias(command):
    # Split the command
    command = command.split(" ")
    alias_parsed={}
    # Check the number of arguments
    if len(command) == 2:
        # equals style
        alias_split = command[1].split("=")
        alias_parsed = {
            "alias": alias_split[0],
            "value": alias_split[1]
        }
    elif len(command) == 3:
        # separate arguments style
        alias_parsed = {
            "alias": command[1],
            "value": command[2]
        }

def cd(command):
    exitcode=0
    # Change the directory
    try:
        split = command.split(" ")
        dir_ = split[1]
        split = dir_.split('/')
        if split[0]=="":
            os.chdir(dir_) # Path is not relative
        else:
            # Crawl down
            for i in range(len(split)):
                dir2 = split.pop()
                os.chdir(os.path.join(os.getcwd(), dir2))
            # Set the exit code and continue
            exitcode = 0    
    except FileNotFoundError:
        exitcode = 1
        print("Could not change directory: No such file or directory")
    
    return exitcode

def pwd():
    print(os.getcwd())