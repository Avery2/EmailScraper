import subprocess
import globals

globals.initialize()

for o in globals.options:
    print(f"{o}: {type(globals.options[o])}")
    if isinstance(globals.options[o], bool):
        print("BOOL")
    elif isinstance(globals.options[o], int):
        print("INT")
    elif isinstance(globals.options[o], str):
        print("STR")

file_to_show = "."
subprocess.call(["open", "-R", file_to_show])
