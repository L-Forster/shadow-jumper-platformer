import time

import pygame as pg
import sys
import random
from distutils.core import setup
import py2exe

setup(    options = {'py2exe': {'includes': ['pygame']}},
          windows = ["main.py"])