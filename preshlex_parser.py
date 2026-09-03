import re
import os
import sys

def parse(command):
    # Substitute variables
    for var in os.environ.keys():
        if re.match(".+(\\{|\\}).+", var):
            continue
        command = re.sub("\\${" + var + "}", os.getenv(var), command)
        command = re.sub(f"\\${var}", os.getenv(var), command)
    
    return command
