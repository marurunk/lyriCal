from src.colors import *
import os
import subprocess

def python_script(script_name:str) -> list | None:
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.join(path, script_name )
    proceso = subprocess.Popen(['python3', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proceso.communicate()
    if proceso.returncode == 0:
        output = stdout.decode().splitlines()
    proceso.kill()
    cRED()
    print(output)
    cWHITE()
    if output[0] == "None" or output == None: 
        return None
    else:
        return output
