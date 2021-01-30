# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simple Project Management TUI                                               #
# A simple TUI (text-based user interface) for logging and keeping track of   #
# things and projects to do, in progress, and completed.                      #
# =========================================================================== #
# IO.py : The IO functions for SPM TUI.                                       #
# =========================================================================== #
# Author: Benjamin Bolling                                                    #
# Creation: 2021-01-29                                                        #
# Author email: benjaminbolling@icloud.com                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from os import remove
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from datetime import datetime

import data.tc as tc

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
        print(f"    {tc.tc.error}Error: Could not find item with name ["+itemName+"] !"+f"{tc.tc.tcend}")
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
            dict[itemName]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = 'Description edited.'
    else:
        print(f"    {tc.tc.error}Error: Could not find item with name ["+itemName+"] !"+f"{tc.tc.tcend}")
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
            print(f"    {tc.tc.error}Error: Could not find item with name ["+itemName+"] !"+f"{tc.tc.tcend}")
    return dict

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
        dict[key]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = 'State changed from '+prevstate+' to Done.'
    else:
        print(f"    {tc.tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tc.tcend}")
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
        print(key+' is now marked as in progress. Previous state was '+prevstate+'.')
        dict[key]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = 'State changed from '+prevstate+' to In Progress.'
    else:
        print(f"    {tc.tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tc.tcend}")
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
        dict[key]['log'][str(datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))] = 'State changed from '+prevstate+' to To-Do..'
    else:
        print(f"    {tc.tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tc.tcend}")
    return dict

def showHelp(commands):
    print(' ')
    print('Possible commands are: ')
    for key in list(commands.keys()):
        print('[ '+str(key)+' ]    '+str(commands[key]))
    print(' ')

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
            print(output+f"{tc.tc.todo}To do.{tc.tc.tcend}")
        elif state == 'ongoing':
            print(output+f"{tc.tc.ongoing}Ongoing.{tc.tc.tcend}")
        elif state == 'done':
            print(output+f"{tc.tc.done}Done.{tc.tc.tcend}")
        else:
            print(output+f"{tc.tc.error}Unkown.{tc.tc.tcend}")
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
        print(f"    {tc.tc.error}Error: Could not find item with name ["+key+"] !"+f"{tc.tc.tcend}")
    print(' ')

def showAll(dict):
    print(' ')
    print(' =========================================================== ')
    print('  All items:'+f"{tc.tc.done} [Done]{tc.tc.ongoing} [In progress]{tc.tc.todo} [To do]{tc.tc.error} [Undefined state]{tc.tc.tcend}")
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
            print(f"    {tc.tc.error}"+key+"     [Error: State could not be read.] "+f"{tc.tc.tcend}")
            print(' ')

def showDone(dict):
    print(' ')
    print('Items done:')
    sorteddict = {i:dict[i] for i in sorted(dict.keys())}
    for key in list(dict.keys()):
        if dict[key]['state'] == 'done':
            print(f"    {tc.tc.done}"+key+f"{tc.tc.tcend}")
            print(' ')

def showTodo(dict):
    print(' ')
    print('Items to do:')
    sorteddict = {i:dict[i] for i in sorted(dict.keys())}
    for key in list(dict.keys()):
        if dict[key]['state'] == 'todo':
            print(f"    {tc.tc.todo}"+key+f"{tc.tc.tcend}")
            print(' ')

def showOngoing(dict):
    print(' ')
    print('Items in progress:')
    sorteddict = {i:dict[i] for i in sorted(dict.keys())}
    for key in list(dict.keys()):
        if dict[key]['state'] == 'ongoing':
            print(f"    {tc.tc.ongoing}"+key+f"{tc.tc.tcend}")
            print(' ')
