#!/usr/bin/env python
from pprint import pprint

DEBUG = False
LOG_LEVEL = 3



def log(value, level=0):
    if level >= LOG_LEVEL:
        pprint(value)