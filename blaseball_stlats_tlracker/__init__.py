"""
blaseball_stlats_tlracker
"""

# Reference:  https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

__version__ = "0.1"

# from .<python file name> import <class name>
from .BST import Player
from .BST import getPlayerStatsByName
from .BST import updatePlayerStatCache
