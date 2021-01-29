from sys import version_info
if version_info < (3, 6):
    raise RuntimeError("This package requres Python 3.6+")

import data.SPM
data.SPM.runtodo()
