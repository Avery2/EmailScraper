import PySimpleGUI as sg
import main
from threading import Thread
import globals
import subprocess
import os
import types

globals.initialize()


class BaseThread(Thread):
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

    def target_with_callback(self, args):
        try:
            self.method(args)
        except Exception as e:
            print(f"{e}\n{'='*10}\n")
            if self.callback is not None:
                if self.callback_args is not None:
                    self.callback(*self.callback_args)
                else:
                    self.callback()
            exit()
        if self.callback is not None:
            if self.callback_args is not None:
                self.callback(*self.callback_args)
            else:
                self.callback()


def createInputLabel(text='ERROR', default_text=""):
    a = sg.Text(text, font="Monaco", s=(15, 1))
    b = sg.Input(key=f"_{text}_", font="Monaco", default_text=default_text)
    return [a, b]


def createInputLabelInt(text='ERROR', default_text=""):
    a = sg.Text(text, font="Monaco", s=(15, 1))
    b = sg.Input(s=(4, 1), key=f"_{text}_", font="Monaco", default_text=default_text)
    return [a, b]


def createCheckboxLabel(text='ERROR', default=False):
    return [sg.Checkbox(text, font="Monaco", key=f"_{text}_", default=default)]


globals.options['disableColors'] = True

options = []
for o in globals.options:
    # Manual GUI elements

    if o == "inputFile":
        options.append([sg.Text('Input File', font="Monaco", s=(15, 1)),
                        sg.InputText('input/TestCaseEmailScript.csv', k="_inputFile_", font="Monaco", s=(30, 1)), sg.FileBrowse()])
        continue

    # Auto GUI from parameters
    if isinstance(globals.options[o], bool):
        options.append(createCheckboxLabel(o, globals.options[o]))
    elif isinstance(globals.options[o], int):
        options.append(createInputLabelInt(o, globals.options[o]))
    elif isinstance(globals.options[o], str):
        options.append(createInputLabel(o, globals.options[o]))

options.sort(key=lambda x: (type(x[0]).__name__, str(len(x))), reverse=True)

initialText = ''
for p in globals.optionNames:
    initialText += f"{p.ljust(25)}None\n"

col1 = [[sg.Frame("Options", layout=options)],
        [sg.Button('Open Output Folder', key="_open_", disabled_button_color="grey", disabled=True),
         sg.Text(size=(40, 1), font="Monaco", key='_outputfile_')]
        ]
col2 = [[sg.Output(size=(100, 45), font="Monaco", echo_stdout_stderr=True, key="_term_")]]
layout = [
    [sg.Column(layout=col1), sg.Column(layout=col2)],
    [sg.Button('Run Search', key="_run_", disabled_button_color="grey"),
     sg.Button('Clear Output', key="_clear_"),
     sg.Button('End Search', key="_terminate_", disabled_button_color="grey", disabled=True),
     sg.Button('Quit', key="_quit_")]]
window = sg.Window('Window Title', layout)


def wrapped_worker(param):
    thread = BaseThread(target=main.main, args=(param,), callback=on_done)
    thread.start()


def on_done():
    window.FindElement("_run_").Update(disabled=False)
    window.FindElement("_open_").Update(disabled=False)
    window.FindElement("_terminate_").Update(disabled=True)
    window['_outputfile_'].update(f"Output file in {globals.output['outputPath']}")
    window.Refresh()


def on_done_terminated():
    window.FindElement("_run_").Update(disabled=False)
    window.Refresh()


while True:
    event, values = window.read()
    param = []
    for p in globals.optionNames:
        val = values[f"_{p}_"] if values else ''
        param.append(f"--{p}")
        param.append(f"{val}")

    if event == sg.WINDOW_CLOSED or event == "_quit_":
        break
    elif event == '_terminate_':
        globals.terminate_early = True
        window.FindElement("_terminate_").Update(disabled=True)
        print(f"\n\n{'!'*15}\nEnding search. Please wait for \"Search Ended\" before starting new search.\n{'!'*15}\n")
        on_done_terminated()
    elif event == "_clear_":
        window.FindElement('_term_').Update('')
    elif event == "_run_":
        wrapped_worker(param)
        window.FindElement("_run_").Update(disabled=True)
        window.FindElement("_open_").Update(disabled=True)
        window.FindElement("_terminate_").Update(disabled=False)
    elif event == "_open_":
        subprocess.call(["open", "-R", globals.output["outputPath"]])

    window.Refresh()

window.close()
os._exit(1)
