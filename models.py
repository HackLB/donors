#!/usr/bin/env python

import app
from pony.orm import *
db = Database("sqlite", "db.sqlite", create_db=True)


class Candidate(db.Entity):
    """
    ORM model representing a unique candidate registered with the FEC.
    """
    committees = Set("Committee")

    CAND_ID = PrimaryKey(unicode)
    CAND_NAME = Optional(unicode, index=True)
    CAND_PTY_AFFILIATION = Optional(unicode, index=True)
    CAND_ELECTION_YR = Optional(unicode)
    CAND_OFFICE_ST = Optional(unicode)
    CAND_OFFICE = Optional(unicode)
    CAND_OFFICE_DISTRICT = Optional(unicode)
    CAND_ICI = Optional(unicode)
    CAND_STATUS = Optional(unicode)
    CAND_PCC = Optional(unicode)
    CAND_ST1 = Optional(unicode)
    CAND_ST2 = Optional(unicode)
    CAND_CITY = Optional(unicode)
    CAND_ST = Optional(unicode)
    CAND_ZIP = Optional(unicode)


class Committee(db.Entity):
    """
    ORM model representing a committee registered with the FEC.
    """
    contributions = Set("Contribution")
    candidates = Set("Candidate")

    CMTE_ID = PrimaryKey(unicode)
    CMTE_NM = Optional(unicode, index=True)
    TRES_NM = Optional(unicode)
    CMTE_ST1 = Optional(unicode)
    CMTE_ST2 = Optional(unicode)
    CMTE_CITY = Optional(unicode)
    CMTE_ST = Optional(unicode)
    CMTE_ZIP = Optional(unicode)
    CMTE_DSGN = Optional(unicode)
    CMTE_TP = Optional(unicode)
    CMTE_PTY_AFFILIATION = Optional(unicode, index=True)
    CMTE_FILING_FREQ = Optional(unicode)
    ORG_TP = Optional(unicode)
    CONNECTED_ORG_NM = Optional(unicode)
    CAND_ID = Optional(unicode)


class Contribution(db.Entity):
    """
    ORM model representing a financial contribution reported to the FEC.
    """
    committee = Optional("Committee")

    CMTE_ID = Optional(unicode)
    AMNDT_IND = Optional(unicode)
    RPT_TP = Optional(unicode)
    TRANSACTION_PGI = Optional(unicode)
    IMAGE_NUM = Optional(unicode)
    TRANSACTION_TP = Optional(unicode)
    ENTITY_TP = Optional(unicode)
    NAME = Optional(unicode)
    CITY = Optional(unicode, index=True)
    STATE = Optional(unicode, index=True)
    ZIP_CODE = Optional(unicode)
    EMPLOYER = Optional(unicode)
    OCCUPATION = Optional(unicode)
    TRANSACTION_DT = Optional(unicode)
    TRANSACTION_AMT = Optional(unicode)
    OTHER_ID = Optional(unicode)
    TRAN_ID = Optional(unicode)
    FILE_NUM = Optional(unicode)
    MEMO_CD = Optional(unicode)
    MEMO_TEXT = Optional(unicode)
    SUB_ID = Optional(unicode)

# turn on debug mode
# sql_debug(True)
 
# map the models to the database 
# and create the tables, if they don't exist
db.generate_mapping(create_tables=True)