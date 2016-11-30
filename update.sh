#!/usr/bin/env bash

dtstamp=$(date +%Y%m%d_%H%M%S)
. ~/.virtualenvs/donors/bin/activate

git pull
./donors.py
git add -A
git commit -m "$dtstamp"
git push

deactivate