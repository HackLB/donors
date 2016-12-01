#!/usr/bin/env python

import app
import os, sys
import simplejson as json
from pprint import pprint
import click


from models import Candidate, Committee, Contribution
from factories import Candidates, Committees, Contributions


def config(loglevel=app.LOG_LEVEL, batchsize=app.BATCH_SIZE):
    app.LOG_LEVEL = int(loglevel)
    app.BATCH_SIZE = int(batchsize)

    current_path = os.path.realpath(sys.argv[0])
    repo_path = os.path.dirname(current_path)     # Path to current directory
    data_path = os.path.join(repo_path, '_data')  # Root path for record data
    os.makedirs(data_path, exist_ok=True)         # Create _data directory


@click.command()
@click.option('--loglevel', default=app.LOG_LEVEL, help='Sets the loglevel.')
@click.option('--batchsize', default=app.BATCH_SIZE, help='Sets the batch size for commits.')
@click.argument('path')
def main(loglevel, batchsize, path):
    config()

    Candidates(os.path.join(path, 'cn.txt'))
    Committees(os.path.join(path, 'cm.txt'))
    Contributions(os.path.join(path, 'indiv16/itcont.txt'))

if __name__ == "__main__":
    main()