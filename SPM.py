# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simple Project Management TUI                                               #
# A simple TUI (text-based user interface) for logging and keeping track of   #
# things and projects to do, in progress, and completed.                      #
# =========================================================================== #
# SPM.py : The main code for running the SPM TUI.                             #
# =========================================================================== #
# Author: Benjamin Bolling                                                    #
# Creation: 2021-01-29                                                        #
# Author email: benjaminbolling@icloud.com                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from json import dump, load
from os import system, listdir, path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from copy import deepcopy

import IO, tc

def runtodo():
    system('clear')

    print(' ')
    print(   f"{tc.tc.blue} ======================================== {tc.tc.tcend}")
    print(f"{tc.tc.magenta}          todoDict python script{tc.tc.tcend}")
    print(f"{tc.tc.magenta}      Simple Project Management tool{tc.tc.tcend}")
    print(    f"{tc.tc.red}  Created 2021-01-28 by Benjamin Bolling{tc.tc.tcend}")
    print(    f"{tc.tc.green}     Email: benjaminbolling@icloud.com{tc.tc.tcend}")
    print(   f"{tc.tc.blue} ======================================== {tc.tc.tcend}")

    files = []
    for file in [f for f in listdir('.') if path.isfile(f)]:
        if file.endswith(".tdDict"):
            files.append(file)
    newOrLoad = str(prompt('Create New or Load a file? [load/new] >> ', completer=WordCompleter(['load','new','quit'])))
    if newOrLoad == 'load' or newOrLoad == 'new':
        if newOrLoad == 'load':
            if len(files) == 1:
                filename = files[0]
            elif len(files) > 1:
                validName = 0
                while validName == 0:
                    filename = str(prompt('Select a file: (use tab completion to see options) >> ', completer=WordCompleter(files)))
                    if filename in files:
                        validName = 1
            else:
                print('No tdDict files found. Creating new.')
                newOrLoad = 'new'

        if newOrLoad == 'new':
            filename = newLogBook(files)
            dict = addItem({})
            savefn(filename,dict)

        with open(filename, 'r') as in_file:
            dict = load(in_file)

        command(filename,dict,1)
        
    elif newOrLoad != 'quit':
        print('Invalid command. Exiting.')

def command(filename,dict,showCommands):
    commands = {'showall':'      Show all tasks',
                'addItem':'      Add a new task',
                'addLog':'       Add a log entry to a task',
                'editItem':'     Edit the description of a task',
                'rmvItem':'      Remove an task',
                'markastodo':'   Change state of a task to "To Do"',
                'markasongoing':'Change state of a task to "Ongoing"',
                'markasdone':'   Change state of a task to "Done"',
                'showitem':'     Show detailed information about a task',
                'showtodo':'     Show all tasks to do',
                'showongoing':'  Show all tasks that are ongoing',
                'showdone':'     Show all tasks that are done',
                'clearOutput':'  Empty the terminal screen',
                'exit':'         Exit the todoDict session',
                'help':'         This help text'}

    if showCommands == 1:
        showHelp(commands)
    print(' ')

    todo = str(prompt('What to do? >> ', completer=WordCompleter(list(commands.keys()))))

    if todo == 'addItem':
        dict = addItem(deepcopy(dict))
    elif todo == 'addLog':
        dict = addLog(deepcopy(dict))
    elif todo == 'editItem':
        dict = editItem(deepcopy(dict))
    elif todo == 'rmvItem':
        dict = rmvItem(deepcopy(dict))

    elif todo == 'showall':
        showAll(deepcopy(dict))
    elif todo == 'showdone':
        showDone(deepcopy(dict))
    elif todo == 'showtodo':
        showTodo(deepcopy(dict))
    elif todo == 'showongoing':
        showOngoing(deepcopy(dict))
    elif todo == 'showitem':
        showItem(deepcopy(dict))

    elif todo == 'markasongoing':
        dict = markItemAsOngoing(deepcopy(dict))
    elif todo == 'markasdone':
        dict = markItemAsDone(deepcopy(dict))
    elif todo == 'markastodo':
        dict = markItemAsTodo(deepcopy(dict))

    elif todo == 'help':
        showHelp(commands)
    elif todo == 'clearOutput':
        system('clear')
    elif todo != 'exit':
        print('Command ['+todo+'] not defined. Try again.')

    if todo == 'exit':
        print(' ')
        print('Exiting todoDict.py.')
        print(' ')
    else:
        if todo in ['addItem','addLog','markastodo','markasongoing','markasdone','editItem','rmvItem']:
            savefn(filename,dict)
        print(' ')
        command(filename,dict,0)

def savefn(filename,dict):
    with open(filename, 'w') as out_file:
        dump(dict, out_file)

runtodo()
