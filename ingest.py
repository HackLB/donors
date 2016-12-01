#!/usr/bin/env python

import app
import os, sys
import simplejson as json
from pprint import pprint
import click


from models import Candidate, Committee, Contribution
from factories import Candidates, Committees, Contributions


def config():
    current_path = os.path.realpath(sys.argv[0])
    repo_path = os.path.dirname(current_path)     # Path to current directory
    data_path = os.path.join(repo_path, '_data')  # Root path for record data
    os.makedirs(data_path, exist_ok=True)         # Create _data directory


@click.command()
@click.option('--loglevel', default=0, help='Sets the loglevel.')
@click.argument('path')
def main(loglevel, path):
    config()
    app.LOG_LEVEL = int(loglevel)

    Candidates(os.path.join(path, 'cn.txt'))
    Committees(os.path.join(path, 'cm.txt'))
    Contributions(os.path.join(path, 'indiv16/itcont.txt'))

if __name__ == "__main__":
    main()