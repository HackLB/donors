#!/usr/bin/env python
import os, sys
import requests
import simplejson as json
from pprint import pprint
import argparse

keys = ['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI','IMAGE_NUM','TRANSACTION_TP','ENTITY_TP','NAME','CITY','STATE','ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID']


def get_subdirectory(base_name):
    """
    Takes the base filename and returns a path to a subdirectory, creating it if needed.
    For example, given the base name 4040720151241706432, returns a path like:
    ./_data/4040720/15/12/41/70/64
    """
    sub_dir = os.path.join(data_path, base_name[0:-12], base_name[-12:-10], base_name[-10:-8], base_name[-8:-6], base_name[-6:-4], base_name[-4:-2])
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir


def save_donor_record(record):
    record_id = record['SUB_ID']
    file_name = '{}.json'.format(record_id)
    directory = get_subdirectory(record_id)

    path = os.path.join(directory, file_name)
    with open(path, 'w') as f:
        json.dump(record, f, indent=4, ensure_ascii=False, sort_keys=True)
    return path


def cleanup(rec):
    rec['AMNDT_IND'] = {'N': 'new', 'A': 'amendment', 'T': 'termination'}.get(rec['AMNDT_IND'])

    rec['RPT_TP'] = {'12C': 'PRE-CONVENTION', '12G': 'PRE-GENERAL', '12P': 'PRE-PRIMARY', '12R': 'PRE-RUN-OFF', '12S': 'PRE-SPECIAL', '30D': 'POST-ELECTION', '30G': 'POST-GENERAL', '30P': 'POST-PRIMARY', '30R': 'POST-RUN-OFF', '30S': 'POST-SPECIAL', '60D': 'POST-CONVENTION', 'ADJ': 'COMP ADJUST AMEND', 'CA': 'COMPREHENSIVE AMEND', 'M10': 'OCTOBER MONTHLY', 'M11': 'NOVEMBER MONTHLY', 'M12': 'DECEMBER MONTHLY', 'M2': 'FEBRUARY MONTHLY', 'M3': 'MARCH MONTHLY', 'M4': 'APRIL MONTHLY', 'M5': 'MAY MONTHLY', 'M6': 'JUNE MONTHLY', 'M7': 'JULY MONTHLY', 'M8': 'AUGUST MONTHLY', 'M9': 'SEPTEMBER MONTHLY', 'MY': 'MID-YEAR REPORT', 'Q1': 'APRIL QUARTERLY', 'Q2': 'JULY QUARTERLY', 'Q3': 'OCTOBER QUARTERLY', 'TER': 'TERMINATION REPORT', 'YE': 'YEAR-END', '90S': 'POST INAUGURAL SUPPLEMENT', '90D': 'POST INAUGURAL', '48H': '48 HOUR NOTIFICATION', '24H': '24 HOUR NOTIFICATION'}.get(rec['RPT_TP'])
    return rec


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))    # Path to current directory
    data_path = os.path.join(repo_path, '_data')                  # Root path for record data
    os.makedirs(data_path, exist_ok=True)                         # Create _data directory

    i = 0
    with open(args.path) as f:
        for line in f:
            donor_rec = dict(zip(keys, [x.strip() for x in line.split('|')]))

            if donor_rec['CITY'] == "LONG BEACH" and donor_rec['STATE'] == "CA":
                donor_rec = cleanup(donor_rec)
                saved_path = save_donor_record(donor_rec)
                print(saved_path)

