#!/usr/bin/env python
from pprint import pprint

DEBUG = False
LOG_LEVEL = 0
BATCH_SIZE = 1000


def log(value, level=0):
    if level >= LOG_LEVEL:
        pprint(value)