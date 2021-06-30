import PySimpleGUI as sg
import main

# ==== GENERAL ====
startRow = 1
numSearch = 5
inputFile = 'input/TestCaseEmailScript.csv'
DO_BING_SEARCH = True
DO_GOOGLE_SEARCH = False
DELAY_SECONDS = 0

# ==== OPTIONS ====
QUOTE_EACH_WORD = True
CREATE_COMBINED = True

# ==== PRIMARY FILTERS ====
DO_PRIMARY_EMAIL_CHECK = True
# SLOW_EMAIL_CHECK = False  # this doesn't actually work rn

# ==== SECONDARY FILTERS ====
APPLY_SECONDARY_FILTERS = True

# ==== DEBUGGING ====
SORT_OUTPUT = True
SHOW_TXT = False
MAKE_LOWERCASE = True


def createInputLabel(str='ERROR', default_text=""):
    a = sg.Text(str)
    b = sg.Input(key=f"-{str}-", default_text=default_text)
    return [a, b]


def createCheckboxLabel(str='ERROR', default=False):
    return [sg.Checkbox(str, key=f"-{str}-", default=default)]


parameters = ["Start Row",
              "Number of Searches",
              "Input File",
              "Bing Search",
              "Google Search",
              "Delay Seconds",
              "Quote Each Word",
              "Create Combined Output File",
              "Do primary email check",
              "Do secondary email check",
              "Sort Output",
              "Show Text",
              "Make Lowercase"]

options = [
    createInputLabel(parameters[0], 1),
    createInputLabel(parameters[1], 5),
    createInputLabel(parameters[2], 'input/TestCaseEmailScript.csv'),
    [sg.Text('Input File'),
     sg.InputText('input/TestCaseEmailScript.csv'), sg.FileBrowse()],
    createCheckboxLabel(parameters[3], True),
    createCheckboxLabel(parameters[4], False),
    createInputLabel(parameters[5], 0),
    createCheckboxLabel(parameters[6], True),
    createCheckboxLabel(parameters[7], True),
    createCheckboxLabel(parameters[8], True),
    createCheckboxLabel(parameters[9], True),
    createCheckboxLabel(parameters[10], True),
    createCheckboxLabel(parameters[11], False),
    createCheckboxLabel(parameters[12], True), ]

# Define the window's contents
layout = [
    [sg.Column(layout=[[sg.Frame("Parameters", layout=options)]]), sg.Column(layout=[[sg.Text(size=(50, 10), key='-OUTPUT-')]])],
    [sg.Button('Run Search'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Window Title', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    allVals = ''
    for param in parameters:
        allVals += param + ": " + str(values[f"-{param}-"])
        allVals += "\n"

    # Output a message to the window
    window['-OUTPUT-'].update(allVals)

# Finish up by removing from the screen
window.close()

# main.main(["main.py"])
