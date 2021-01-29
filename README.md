# Simple Project Management TUI.
A simple TUI (text-based user interface) for logging and keeping track of things and projects to do, in progress, and completed.

# Package history
Original author is Benjamin Bolling, (ORCID iD 0000-0002-6650-5365)[https://orcid.org/0000-0002-6650-5365].

Package development began 2021-01-28, version 1 finished 2021-01-30.

# Setup
Requires python 3.6 or higher.

Execute `pip install -r requirements.txt` to install python packages required.

# Launch SPM TUI
Execute `python runSPM.py` to start running the package.

# How-to-use
The TUI has tab-completion implemented to aid the user. At start-up, the user is prompted to either create a new file [ `new` ] or to load a previously created file [ `load` ]. The file extension is `.tdDict`, which stands for *to-do dictionary*. In the rest of the TUI session, the user can use the list of commands defined in Table 1.

Table 1: Implemented commands and their meaning.
| Command | Meaning |
| :----------: | :----------: |
| `showall` | Show all tasks |
| `addItem` | Add a new task |
| `addLog` | Add a log entry to a task |
| `editItem` | Edit the description of a task |
| `rmvItem` | Remove an task |
| `markastodo` | Change state of a task to "To Do" |
| `markasongoing` | Change state of a task to "Ongoing" |
| `markasdone` | Change state of a task to "Done" |
| `showitem` | Show detailed information about a task |
| `showtodo` | Show all tasks to do |
| `showongoing` | Show all tasks that are ongoing |
| `showdone` | Show all tasks that are done |
| `clearOutput` | Empty the terminal screen |
| `exit` | Exit the todoDict session |
| `help` | A help text |
