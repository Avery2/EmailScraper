import PySimpleGUI as sg
import main
from threading import Thread
import globals

globals.initialize()


def createInputLabel(str='ERROR', default_text=""):
    a = sg.Text(str)
    b = sg.Input(key=f"_{str}_", default_text=default_text)
    return [a, b]


def createCheckboxLabel(str='ERROR', default=False):
    return [sg.Checkbox(str, key=f"_{str}_", default=default)]


globals.options['disableColors'] = True

options = []
for o in globals.options:
    if isinstance(globals.options[o], bool):
        options.append(createCheckboxLabel(o, globals.options[o]))
    elif isinstance(globals.options[o], int):
        options.append(createInputLabel(o, globals.options[o]))
    elif isinstance(globals.options[o], str):
        options.append(createInputLabel(o, globals.options[o]))

col1 = [[sg.Frame("Parameters", layout=options)], [sg.Text(size=(60, 10), font="Monaco", key='_output_')]]
col2 = [[sg.Output(size=(80, 30), font="Monaco", echo_stdout_stderr=True, key="_term_")]]
layout = [
    [sg.Column(layout=col1), sg.Column(layout=col2)],
    [sg.Button('Run Search', key="_run_", disabled_button_color="grey"), sg.Button('Clear Output', key="_clear_")]]
window = sg.Window('Window Title', layout)


def wrapped_worker(param):
    worker(param)
    on_done()


def on_done():
    window.FindElement("_run_").Update(disabled=False)


def worker(param):
    thread = Thread(target=main.main, args=(param,))
    thread.start()


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    param = []
    allVals = ''
    for p in globals.optionNames:
        val = values[f"_{p}_"]
        allVals += f"{p.ljust(25)}{str(val)}\n"
        # try:
        #     val = int(val)
        # except ValueError:
        #     pass
        # globals.options[p] = val
        param.append(f"--{p}")
        param.append(f"{val}")

    if event == "_clear_":
        window.FindElement('_term_').Update('')

    if event == "_run_":
        wrapped_worker(param)
        # window.FindElement("_run_").Update(disabled=True)

    window['_output_'].update(allVals)
    window.Refresh()

window.close()
