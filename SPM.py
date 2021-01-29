# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simple Project Management                                                   #
# A tool for logging and keeping track of things to do.                       #
# =========================================================================== #
# Author: Benjamin Bolling                                                    #
# Creation: 2021-01-29                                                        #
# Author email: benjaminbolling@icloud.com                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from json import dump, load
from os import system, remove, listdir, path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from copy import deepcopy
from datetime import datetime

class tc:
    # text color
    magenta = '\033[95m'
    blue = '\033[90m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'

    bold = '\033[1m'
    underline = '\033[4m'

    tcend = '\033[0m'

    todo = yellow
    ongoing = cyan
    done = green
    error = red

def newLogBook(files):
    accepted = 0
    while accepted == 0:
        filename = str(input('Define name of new to-do list: >> '))
        if filename in files:
            if str(input('Logbook already exists. Overwrite? Warning: This action is irreversible. [y/N] >> ')) == 'y':
                remove(filename)
                accepted = 1
        else:
            accepted = 1
    if filename.endswith(".tdDict"):
        return filename
    else:
        return filename+".tdDict"

def runtodo():
    system('clear')

    print(' ')
    print(   f"{tc.blue} ======================================== {tc.tcend}")
    print(f"{tc.magenta}          todoDict python script{tc.tcend}")
    print(    f"{tc.red}  Created 2021-01-28 by Benjamin Bolling{tc.tcend}")
    print(    f"{tc.green}     Email: benjaminbolling@icloud.com{tc.tcend}")
    print(   f"{tc.blue} ======================================== {tc.tcend}")

    files = []
    for file in [f for f in listdir('.') if path.isfile(f)]:
        if file.endswith(".tdDict"):
            files.append(file)

    newOrLoad = str(prompt('Create New or Load a file? [load/new] >> ', completer=WordCompleter(['load','new'])))
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
    else:
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

def showHelp(commands):
    print(' ')
    print('Possible commands are: ')
    for key in list(commands.keys()):
        print('[ '+str(key)+' ]    '+str(commands[key]))
    print(' ')

def getNewItemName(dict):
    itemName = str(input('Define new task: >> '))
    ok = 1
    if itemName in list(dict.keys()):
        ok = 0
    if ok == 0:
        overwrite = 'x'
        while overwrite not in ['y','n']:
            overwrite  = input('Object already exists. Overwrite? [y/n] >> ')
        if overwrite == 'y':
            dict.pop(itemName, None)
            ok = 1
    if ok == 1:
        return itemName
    else:
        return getNewItemName(filename,dict)

def addItem(dict):
    itemName = getNewItemName(dict)
    itemDescription = input('Write a description of the task: >> ')
    itemState = 'todo'
    dict[itemName] = {'state':itemState,'description':itemDescription}
    dict[itemName]['log'] = {}
    dict[itemName]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = 'Item created.'
    return dict

def addLog(dict):
    showAll(dict)
    print(' ')
    print(' =================================== ')
    print(' ')
    itemName = str(prompt('Insert the name of the item to insert a log entry to: >> ', completer=WordCompleter(list(dict.keys()))))
    if itemName in list(dict.keys()):
        logs = dict[itemName]['log']
        for logentry in list(logs.keys()):
            print(str(logentry)+' : '+str(logs[logentry]))
        newLogEntry = input('Log entry for '+itemName+': >> ')
        dict[itemName]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = newLogEntry
    else:
        print(f"    {tc.error}Error: Could not find item with name ["+itemName+"] !"+f"{tc.tcend}")
    return dict

def editItem(dict):
    showAll(dict)
    print(' ')
    print(' =================================== ')
    print(' ')
    itemName = str(prompt('Insert the name of the item which is to be edited: >> ', completer=WordCompleter(list(dict.keys()))))
    if itemName in list(dict.keys()):
        print('Current description:')
        print(str(dict[itemName]['description']))
        print(' ')
        newdescription = input('New description for '+itemName+': >> ')
        if input('Confirm new description for '+itemName+': [y/N] >>') == 'y':
            dict[itemName]['description'] = newdescription
            dict[itemName]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = 'Description of item edited.'
    else:
        print(f"    {tc.error}Error: Could not find item with name ["+itemName+"] !"+f"{tc.tcend}")
    return dict

def rmvItem(dict):
    showAll(dict)
    print(' ')
    print(' =================================== ')
    print(' ')
    if input('Warning: This process is irreversible. Continue? [y/N] >> ') == 'y':
        itemName = str(prompt('Insert the name of the item which is to be removed: >> ', completer=WordCompleter(list(dict.keys()))))
        if itemName in list(dict.keys()):
            if input('Confirm removal of '+itemName+': [y/N] >>') == 'y':
                del dict[itemName]
                print(itemName+' deleted.')
        else:
            print(f"    {tc.error}Error: Could not find item with name ["+itemName+"] !"+f"{tc.tcend}")
    return dict

def showItem(dict):
    showAll(dict)
    print(' ')
    print(' =================================== ')
    print(' ')
    key = prompt('Insert the name of the item to show: >> ', completer=WordCompleter(list(dict.keys())))
    if key in list(dict.keys()):
        state = str(dict[key]['state'])
        print(' ')
        print('Item shown: '+key)
        print(' ')
        output = 'State: '
        if state == 'todo':
            print(output+f"{tc.todo}To do.{tc.tcend}")
        elif state == 'ongoing':
            print(output+f"{tc.ongoing}Ongoing.{tc.tcend}")
        elif state == 'done':
            print(output+f"{tc.done}Done.{tc.tcend}")
        else:
            print(output+f"{tc.error}Unkown.{tc.tcend}")
        print(' ')
        description = str(dict[key]['description'])
        for row in description.split('\\n'):
            if len(row) > 0:
                print(row)
        print(' ')
        print(' =================================== ')
        print(' ')
        print('Logs:')
        print(' ')
        logs = dict[key]['log']
        for logentry in list(logs.keys()):
            print(str(logentry)+' : '+str(logs[logentry]))
        print(' ')
        print(' =================================== ')
        print(' ')
    else:
        print(f"    {tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
    print(' ')

def showAll(dict):
    print(' ')
    print(' =========================================================== ')
    print('  All items:'+f"{tc.done} [Done]{tc.ongoing} [In progress]{tc.todo} [To do]{tc.error} [Undefined state]{tc.tcend}")
    print(' =========================================================== ')
    showOngoing(dict)
    showTodo(dict)
    showDone(dict)
    showUnknowns(dict)
    print(' ')

def showUnknowns(dict):
    print(' ')
    print('Items in an unknown state:')
    for key in list(dict.keys()):
        if dict[key]['state'] not in ['done','todo','ongoing']:
            print(f"    {tc.error}"+key+"     [Error: State could not be read.] "+f"{tc.tcend}")
            print(' ')

def showDone(dict):
    print(' ')
    print('Items done:')
    sorteddict = {i:dict[i] for i in sorted(dict.keys())}
    for key in list(dict.keys()):
        if dict[key]['state'] == 'done':
            print(f"    {tc.done}"+key+f"{tc.tcend}")
            print(' ')

def showTodo(dict):
    print(' ')
    print('Items to do:')
    sorteddict = {i:dict[i] for i in sorted(dict.keys())}
    for key in list(dict.keys()):
        if dict[key]['state'] == 'todo':
            print(f"    {tc.todo}"+key+f"{tc.tcend}")
            print(' ')

def showOngoing(dict):
    print(' ')
    print('Items in progress:')
    sorteddict = {i:dict[i] for i in sorted(dict.keys())}
    for key in list(dict.keys()):
        if dict[key]['state'] == 'ongoing':
            print(f"    {tc.ongoing}"+key+f"{tc.tcend}")
            print(' ')

def markItemAsDone(dict):
    showTodo(dict)
    showOngoing(dict)
    showUnknowns(dict)
    print(' ')
    print(' ')
    key = str(prompt('Insert the name of the item which is done: >> ', completer=WordCompleter(list(dict.keys()))))
    if key in list(dict.keys()):
        prevstate = str(dict[key]['state'])
        dict[key]['state'] = 'done'
        print(key+' is now marked as done. Previous state was '+prevstate+'.')
        dict[itemName]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = 'State changed from '+prevstate+' to done.'
    else:
        print(f"    {tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
    return dict

def markItemAsOngoing(dict):
    showTodo(dict)
    showDone(dict)
    showUnknowns(dict)
    print(' ')
    print(' ')
    key = str(prompt('Insert the name of the item which is ongoing: >> ', completer=WordCompleter(list(dict.keys()))))
    if key in list(dict.keys()):
        prevstate = str(dict[key]['state'])
        dict[key]['state'] = 'ongoing'
        print(key+' is now marked as done. Previous state was '+prevstate+'.')
    else:
        print(f"    {tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
    return dict

def markItemAsTodo(dict):
    showOngoing(dict)
    showDone(dict)
    showUnknowns(dict)
    print(' ')
    print(' ')
    key = str(prompt('Insert the name of the item which is on the to-do list: >> ', completer=WordCompleter(list(dict.keys()))))
    if key in list(dict.keys()):
        prevstate = str(dict[key]['state'])
        dict[key]['state'] = 'todo'
        print(key+' is now marked as todo. Previous state was '+prevstate+'.')
    else:
        print(f"    {tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
    return dict

def savefn(filename,dict):
    with open(filename, 'w') as out_file:
        dump(dict, out_file)

runtodo()
