import PySimpleGUI as sg
import main
from threading import Thread
import globals

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


def createInputLabel(str='ERROR', default_text=""):
    a = sg.Text(str, font="Monaco")
    b = sg.Input(key=f"_{str}_", font="Monaco", default_text=default_text)
    return [a, b]


def createCheckboxLabel(str='ERROR', default=False):
    return [sg.Checkbox(str, font="Monaco", key=f"_{str}_", default=default)]


globals.options['disableColors'] = True

options = []
for o in globals.options:
    # Manual GUI elements

    if o == "inputFile":
        options.append([sg.Text('Input File', font="Monaco"),
                        sg.InputText('input/TestCaseEmailScript.csv', k="_inputFile_", font="Monaco"), sg.FileBrowse()])
        continue

    # Auto GUI from parameters
    if isinstance(globals.options[o], bool):
        options.append(createCheckboxLabel(o, globals.options[o]))
    elif isinstance(globals.options[o], int):
        options.append(createInputLabel(o, globals.options[o]))
    elif isinstance(globals.options[o], str):
        options.append(createInputLabel(o, globals.options[o]))

col1 = [[sg.Frame("Parameters", layout=options)],
        [sg.Text(size=(60, 10), font="Monaco", key='_output_')],
        [sg.Text(size=(20, 10), font="Monaco", key='_outputfile_')]]
col2 = [[sg.Output(size=(100, 45), font="Monaco", echo_stdout_stderr=True, key="_term_")]]
layout = [
    [sg.Column(layout=col1), sg.Column(layout=col2)],
    [sg.Button('Run Search', key="_run_", disabled_button_color="grey"), sg.Button('Clear Output', key="_clear_")]]
window = sg.Window('Window Title', layout)


def wrapped_worker(param):
    thread = BaseThread(target=main.main, args=(param,), callback=on_done)
    thread.start()


def on_done():
    window.FindElement("_run_").Update(disabled=False)


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    param = []
    allVals = ''
    for p in globals.optionNames:
        val = values[f"_{p}_"]
        allVals += f"{p.ljust(25)}{str(val)}\n"
        param.append(f"--{p}")
        param.append(f"{val}")

    if event == "_clear_":
        window.FindElement('_term_').Update('')

    if event == "_run_":
        wrapped_worker(param)
        window.FindElement("_run_").Update(disabled=True)

    window['_output_'].update(allVals)
    window['_outputfile_'].update("OUTPUT")
    window.Refresh()

window.close()
