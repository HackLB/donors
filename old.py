#!/usr/bin/env python

import app
import os, sys
import simplejson as json
from pprint import pprint
import click


from models import Candidate, Committee, Contribution
from factories import Candidates, Committees, Contributions


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
    record_id = str(record['SUB_ID'])
    file_name = '{}.json'.format(record_id)
    directory = get_subdirectory(record_id)

    path = os.path.join(directory, file_name)
    with open(path, 'w') as f:
        json.dump(record, f, indent=4, ensure_ascii=False, sort_keys=True)
    return path


def cleanup(record):

    # Set empty values to None
    for key in record:
        if len(record[key]) == 0:
            record[key] = None

    record['parsed'] = {}

    record['parsed']['AMNDT_IND'] = {'N': 'new', 'A': 'amendment', 'T': 'termination'}.get(record['AMNDT_IND'])

    record['parsed']['RPT_TP'] = {'12C': 'PRE-CONVENTION', '12G': 'PRE-GENERAL', '12P': 'PRE-PRIMARY', '12R': 'PRE-RUN-OFF', '12S': 'PRE-SPECIAL', '30D': 'POST-ELECTION', '30G': 'POST-GENERAL', '30P': 'POST-PRIMARY', '30R': 'POST-RUN-OFF', '30S': 'POST-SPECIAL', '60D': 'POST-CONVENTION', 'ADJ': 'COMP ADJUST AMEND', 'CA': 'COMPREHENSIVE AMEND', 'M10': 'OCTOBER MONTHLY', 'M11': 'NOVEMBER MONTHLY', 'M12': 'DECEMBER MONTHLY', 'M2': 'FEBRUARY MONTHLY', 'M3': 'MARCH MONTHLY', 'M4': 'APRIL MONTHLY', 'M5': 'MAY MONTHLY', 'M6': 'JUNE MONTHLY', 'M7': 'JULY MONTHLY', 'M8': 'AUGUST MONTHLY', 'M9': 'SEPTEMBER MONTHLY', 'MY': 'MID-YEAR REPORT', 'Q1': 'APRIL QUARTERLY', 'Q2': 'JULY QUARTERLY', 'Q3': 'OCTOBER QUARTERLY', 'TER': 'TERMINATION REPORT', 'YE': 'YEAR-END', '90S': 'POST INAUGURAL SUPPLEMENT', '90D': 'POST INAUGURAL', '48H': '48 HOUR NOTIFICATION', '24H': '24 HOUR NOTIFICATION'}.get(record['RPT_TP'])

    record['parsed']['TRANSACTION_PGI'] = {'P': 'Primary', 'G': 'General', 'O': 'Other', 'C': 'Convention', 'R': 'Runoff', 'S': 'Special', 'E': 'Recount'}.get(record['TRANSACTION_PGI'])

    record['parsed']['TRANSACTION_TP'] = {'10': 'Contribution to Independent Expenditure-Only Committees (Super PACs), Political Committees with non-contribution accounts (Hybrid PACs) and nonfederal party \"soft money\" accounts (1991-2002) from a person (individual, partnership, limited liability company, corporation, labor organization, or any other organization or group of persons)', '10J': 'Memo - Recipient committee\'s percentage of nonfederal receipt from a person (individual, partnership, limited liability company, corporation, labor organization, or any other organization or group of persons)', '11': 'Native American Tribe contribution', '11J': 'Memo - Recipient committee\'s percentage of contribution from Native American Tribe given to joint fundraising committee', '12': 'Nonfederal other receipt - Levin Account (Line 2)', '13': 'Inaugural donation accepted', '15': 'Contribution to political committees (other than Super PACs and Hybrid PACs) from an individual, partnership or limited liability company', '15C': 'Contribution from candidate', '15E': 'Earmarked contributions to political committees (other than Super PACs and Hybrid PACs) from an individual, partnership or limited liability company', '15F': 'Loans forgiven by candidate', '15I': 'Earmarked contribution from an individual, partnership or limited liability company received by intermediary committee and passed on in the form of contributor\'s check (intermediary in)', '15J': 'Memo - Recipient committee\'s percentage of contribution from an individual, partnership or limited liability company given to joint fundraising committee', '15T': 'Earmarked contribution from an individual, partnership or limited liability company received by intermediary committee and entered into intermediary\'s treasury (intermediary treasury in)', '15Z': 'In-kind contribution received from registered filer', '16C': 'Loan received from the candidate', '16F': 'Loan received from bank', '16G': 'Loan from individual', '16H': 'Loan from registered filers', '16J': 'Loan repayment from individual', '16K': 'Loan repayment from from registered filer', '16L': 'Loan repayment received from unregistered entity', '16R': 'Loan received from registered filers', '16U': 'Loan received from unregistered entity', '17R': 'Contribution refund received from registered entity', '17U': 'Refund/Rebate/Return received from unregistered entity', '17Y': 'Refund/Rebate/Return from individual or corporation', '17Z': 'Refund/Rebate/Return from candidate or committee', '18G': 'Transfer in from affiliated committee', '18H': 'Honorarium received', '18J': 'Memo - Recipient committee\'s percentage of contribution from a registered committee given to joint fundraising committee', '18K': 'Contribution received from registered filer', '18L': 'Bundled contribution', '18U': 'Contribution received from unregistered committee', '19': 'Electioneering communication donation received', '19J': 'Memo - Recipient committee\'s percentage of Electioneering Communication donation given to joint fundraising committee', '20': 'Nonfederal disbursement - nonfederal party \"soft money\" accounts (1991-2002)', '20A': 'Nonfederal disbursement - Levin Account (Line 4A) Voter Registration', '20B': 'Nonfederal Disbursement - Levin Account (Line 4B) Voter Identification', '20C': 'Loan repayment made to candidate', '20D': 'Nonfederal disbursement - Levin Account (Line 4D) Generic Campaign', '20F': 'Loan repayment made to banks', '20G': 'Loan repayment made to individual', '20R': 'Loan repayment made to registered filer', '20V': 'Nonfederal disbursement - Levin Account (Line 4C) Get Out The Vote', '20Y': 'Nonfederal refund', '21Y': 'Native American Tribe refund', '22G': 'Loan to individual', '22H': 'Loan to candidate or committee', '22J': 'Loan repayment to individual', '22K': 'Loan repayment to candidate or committee', '22L': 'Loan repayment to bank', '22R': 'Contribution refund to unregistered entity', '22U': 'Loan repaid to unregistered entity', '22X': 'Loan made to unregistered entity', '22Y': 'Contribution refund to an individual, partnership or limited liability company', '22Z': 'Contribution refund to candidate or committee', '23Y': 'Inaugural donation refund', '24A': 'Independent expenditure opposing election of candidate'}.get(record['TRANSACTION_TP'])

    record['parsed']['ENTITY_TP'] = {'CAN': 'Candidate', 'CCM': 'Candidate Committee', 'COM': 'Committee', 'IND': 'Individual (a person)', 'ORG': 'Organization (not a committee and not a person)', 'PAC': 'Political Action Committee', 'PTY': 'Party Organization'}.get(record['ENTITY_TP'])

    # Fix zipcode formatting for ZIP+9
    if len(record['ZIP_CODE']) == 9:
        record['ZIP_CODE'] = '{}-{}'.format(record['ZIP_CODE'][0:5], record['ZIP_CODE'][5:10])

    record['FILE_NUM'] = int(record['FILE_NUM'])
    record['SUB_ID'] = int(record['SUB_ID'])

    return record




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

    i = 0
    with open(path) as f:
        for line in f:
            donor_rec = dict(zip(keys, [x.strip() for x in line.split('|')]))

            if donor_rec['CITY'] == "LONG BEACH" and donor_rec['STATE'] == "CA":
                donor_rec = cleanup(donor_rec)
                saved_path = save_donor_record(donor_rec)
                pprint(donor_rec)
                print(saved_path)


if __name__ == "__main__":
    main()
