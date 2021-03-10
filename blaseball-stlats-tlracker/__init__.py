"""
blaseball_stlats_tlracker
"""

# Reference:  https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

__version__ = "0.1"


import os

try:
    dirs = ["cache"]
    cwd = os.getcwd()
    for dir in dirs:
        abs_dir = os.path.join(cwd, dir)
        if not os.path.exists(abs_dir):
            os.mkdir(abs_dir)
except:
    print('Directory creation failed.')
    exit(-1)
