import subprocess
import my_globals

my_globals.initialize()

for o in my_globals.options:
    print(f"{o}: {type(my_globals.options[o])}")
    if isinstance(my_globals.options[o], bool):
        print("BOOL")
    elif isinstance(my_globals.options[o], int):
        print("INT")
    elif isinstance(my_globals.options[o], str):
        print("STR")

file_to_show = "."
# subprocess.call(["open", "-R", file_to_show])
