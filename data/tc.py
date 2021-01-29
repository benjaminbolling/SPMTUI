# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simple Project Management TUI                                               #
# A simple TUI (text-based user interface) for logging and keeping track of   #
# things and projects to do, in progress, and completed.                      #
# =========================================================================== #
# tc.py : The text color class for SPM TUI.                                   #
# =========================================================================== #
# Author: Benjamin Bolling                                                    #
# Creation: 2021-01-29                                                        #
# Author email: benjaminbolling@icloud.com                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class tc: # text color
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
