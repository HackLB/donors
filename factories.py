#!/usr/bin/env python

import app
from models import Candidate, Committee, Contribution
import pony.orm as pony
from pprint import pprint

class Candidates(object):
    """
    ORM model representing a unique candidate registered with the FEC.
    """
    model = Candidate
    candidates = []

    keys = ['CAND_ID', 'CAND_NAME', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 'CAND_OFFICE_ST', 'CAND_OFFICE', 'CAND_OFFICE_DISTRICT', 'CAND_ICI', 'CAND_STATUS', 'CAND_PCC', 'CAND_ST1', 'CAND_ST2', 'CAND_CITY', 'CAND_ST', 'CAND_ZIP']

    @pony.db_session
    def __init__(self, path):
        self.path = path

        i = 1
        with open(path) as f:
            for line in f:
                app.log('candidate: {}'.format(i), level=3)
                candidate_record = dict(zip(self.keys, [x.strip() for x in line.split('|')]))
                app.log(candidate_record)

                try:
                    Candidate(**candidate_record)
                except pony.core.CacheIndexError:
                    pass
                except pony.core.TransactionIntegrityError:
                    pass

                i += 1


class Committees(object):
    """
    ORM model representing a committee registered with the FEC.
    """
    model = Committee
    committees = []

    keys = ['CMTE_ID', 'CMTE_NM', 'TRES_NM', 'CMTE_ST1', 'CMTE_ST2', 'CMTE_CITY', 'CMTE_ST', 'CMTE_ZIP', 'CMTE_DSGN', 'CMTE_TP', 'CMTE_PTY_AFFILIATION', 'CMTE_FILING_FREQ', 'ORG_TP', 'CONNECTED_ORG_NM', 'CAND_ID']

    @pony.db_session
    def __init__(self, path):
        self.path = path

        i = 1
        with open(path) as f:
            for line in f:
                app.log('committee: {}'.format(i), level=3)
                committee_record = dict(zip(self.keys, [x.strip() for x in line.split('|')]))
                app.log(committee_record)

                try:
                    Committee(**committee_record)
                except pony.core.CacheIndexError:
                    pass
                except pony.core.TransactionIntegrityError:
                    pass

                i += 1


class Contributions(object):
    """
    ORM model representing a financial contribution reported to the FEC.
    """
    model = Contribution
    contributions = []

    keys = ['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI','IMAGE_NUM','TRANSACTION_TP','ENTITY_TP','NAME','CITY','STATE','ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID']

    @pony.db_session
    def __init__(self, path):
        self.path = path

        i = 1
        with open(path) as f:
            for line in f:
                app.log('contrib: {}'.format(i), level=3)
                contribution_record = dict(zip(self.keys, [x.strip() for x in line.split('|')]))
                # if contribution_record['CITY'] == "LONG BEACH" and contribution_record['STATE'] == "CA":
                if True:
                    # app.log(contribution_record)
                    this_contrib = Contribution(**contribution_record)
                    this_committee = Committee.get(CMTE_ID=this_contrib.CMTE_ID)
                    this_contrib.committee = this_committee
                i += 1