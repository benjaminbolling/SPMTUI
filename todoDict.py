# To Do Dicts
# 2021 Benjamin Bolling, European Spallation Source ERIC
from json import dump, load
from os import system
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from copy import deepcopy

class tc:
    # text color
    magenta = '\033[95m'
    blue = '\033[94m'
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

filename = 'dict01.data'

with open(filename, 'r') as in_file:
    dict = load(in_file)

system('clear')

def command(filename,dict):
    commands = ['add','showall','showitem','showtodo','showongoing','showdone','markastodo','markasongoing','markasdone','edit','rmv','clearOutput','exit']
    commandsStr = ''
    for c in commands:
        commandsStr = commandsStr + '['+c+'] '
    print(' ')
    print('Possible commands are in brackets: '+commandsStr)
    print(' ')

    todo = str(prompt('What to do? >> ', completer=WordCompleter(commands)))

    if todo == 'add':
        dict = addItem(deepcopy(dict))
    elif todo == 'edit':
        dict = editItem(deepcopy(dict))
    elif todo == 'rmv':
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

    elif todo == 'clearOutput':
        system('clear')
    elif todo != 'exit':
        print('Command ['+todo+'] not defined. Try again.')

    if todo == 'exit':
        print(' ')
        print('Exiting todoDict.py.')
        print(' ')
    else:
        if todo in ['add','markastodo','markasongoing','markasdone','edit','rmv']:
            savefn(filename,dict)
        print(' ')
        command(filename,dict)

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
    return dict

def editItem(dict):
    itemName = str(prompt('Insert the name of the item which is to be edited: >> ', completer=WordCompleter(list(dict.keys()))))
    if itemName in list(dict.keys()):
        print('Current description:')
        print(str(dict[itemName]['description']))
        print(' ')
        newdescription = input('New description for '+itemName+': >> ')
        if input('Confirm new description for '+itemName+': [y/N] >>') == 'y':
            dict[itemName]['description'] = newdescription
    return dict

def rmvItem(dict):
    if input('Warning: This process is irreversible. Continue? [y/N] >> ') == 'y':
        itemName = str(prompt('Insert the name of the item which is to be removed: >> ', completer=WordCompleter(list(dict.keys()))))
        if itemName in list(dict.keys()):
            if input('Confirm removal of '+itemName+': [y/N] >>') == 'y':
                del dict[itemName]
                print(itemName+' deleted.')
        else:
            print(itemName+' not found.')
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
    else:
        print(f"{tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
    print(' ')

def showAll(dict):
    print(' ')
    print('All items: '+f"{tc.done} [Done]{tc.ongoing} [In progress]{tc.todo} [To do]{tc.error} [Undefined state]{tc.tcend}")
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
            print(f"{tc.error}"+key+"     [Error: State could not be read.] "+f"{tc.tcend}")
            print(' ')

def showDone(dict):
    print(' ')
    print('Items done:')
    for key in list(dict.keys()):
        if dict[key]['state'] == 'done':
            print(f"{tc.done}"+key+f"{tc.tcend}")
            print(' ')

def showTodo(dict):
    print(' ')
    print('Items to do:')
    for key in list(dict.keys()):
        if dict[key]['state'] == 'todo':
            print(f"{tc.todo}"+key+f"{tc.tcend}")
            print(' ')

def showOngoing(dict):
    print(' ')
    print('Items in progress:')
    for key in list(dict.keys()):
        if dict[key]['state'] == 'ongoing':
            print(f"{tc.ongoing}"+key+f"{tc.tcend}")
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
    else:
        print(f"{tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
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
        print(f"{tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
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
        print(f"{tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tcend}")
    return dict

def savefn(filename,dict):
    with open(filename, 'w') as out_file:
        dump(dict, out_file)

command(filename,dict)
