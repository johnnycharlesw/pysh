import shlex
import subprocess
import preshlex_parser
import pysh_builtins

def split_pipeline(command):
    commands = []
    for part in command.split("|"):
        lexed = preshlex_parser.parse(part)
        if len(lexed) < 1:
            continue
        else:
            commands.append(shlex.split(part))
    return commands

def execute_posix(command):
    commands = split_pipeline(command=command)
    
    processes = []
    previous_stdout = None

    interpreters = ["pysh", "bash", "ksh", "zsh", "sh", "python3", "node", "php", "cmd"]

    is_first=True
    for command in commands:

        if is_first == True:
            is_first = False
            continue

        if " ".join(command) in interpreters:
            print("""
The command you typed was found, but it cannot be executed for security reasons because you piped a script into an interpreter.

Piping into interpreters is blocked to prevent accidental execution of untrusted scripts.
Generally, don't do this:
```sh
curl https://site.sh/script | sh
```

Do this instead:
```sh
wget https://site.sh/script
codium script # review it first!
sh script
```
            """)
            exitcode = -2
            return

    for cmd in commands:
        process = subprocess.Popen(
            cmd,
            stdin=previous_stdout,
            stdout=subprocess.PIPE
        )

        if previous_stdout is not None:
            previous_stdout.close()

        previous_stdout = process.stdout
        processes.append(process)

    if not processes:
        return
    

    output, _ = processes[-1].communicate()

    for process in processes[:-1]:
        process.wait()

    if output:
        print(output.decode(errors="replace"), end="")

    return processes[-1].returncode

def execute_python(command):
    try:
        exec(command)
        exitcode = 0
    except Exception:
        print("Command not found, or an exception occured.")
        exitcode=-1
    return exitcode

def run_command(command):
    try:
        split = shlex.split(command)
        if split[0] == "exit":
            try:
                pysh_builtins.exit_(split[1]) # The exit command is needed to exit the shell
            except IndexError:
                pysh_builtins.exit_(0)
        if split[0] == "cd":
            pysh_builtins.cd(command)
            return
    
        if split[0] == "pwd":
            pysh_builtins.pwd()
            return
        
        execute_posix(command)
    except Exception:
        execute_python(command)

def execute_script(path):
    try:
        fd = open(path,'r')
        commands = fd.readlines()
        for command in commands:
            run_command(command)
    except FileNotFoundError:
        print(f"Script not found: {path}")