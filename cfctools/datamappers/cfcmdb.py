# ======================================================================
# Class: CfcMdb:
# - For accessing the cfc*.mdb Microsoft Access database files.
# - cfc*.mdb files are the legacy (1997 to 2021) main CFC database.
#   - For schema, see notes at bottom of this file.
#   - since are old file format must use old 32-bit MS-Access driver.
#   - since old 32-bit driver must run under 32-bit Python.
# - MS-Access files are accessed using the pyodbc package
#   - Ref: https://github.com/mkleehammer/pyodbc/wiki/Tips-and-Tricks-by-Database-Platform
# ======================================================================
import pyodbc
from ..common.models.member import Member
from ..common.models.event import Event
from ..common.models.event_result import EventResult


class CfcMdb:
    def __init__(self, file, password=None):
        self._file = str(file)
        self._password = password
        self._dbconn = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if callable(getattr(self._dbconn, 'close', None)):
            self._dbconn.close()

    def _get_dbconn(self):
        if self._dbconn is None:
            pyodbc.pooling = False
            driver = '{Microsoft Access Driver (*.mdb)}'
            dbdsn = f'DRIVER={driver};DBQ={self._file};'    # error if DBQ has quotes
            if self._password:
                dbdsn += f'PWD={self._password};'
            self._dbconn = pyodbc.connect(dbdsn)
        return self._dbconn

    def fetch_all_members(self, sort=None):
        sort = sort or '[NUMBER]'
        table = 'Membership Information'

        dbcsr = self._get_dbconn().cursor()
        sql = f'select * from [{table}] order by {sort}'
        dbcsr.execute(sql)
        for row in dbcsr.fetchall():
            yield _mdb_to_member(row)
        dbcsr.close()

    def fetch_events_for_year(self, year, sort=None):
        year = int(year)
        sort = sort or '[TOURN NUMBER], [FINISH POSITION]'
        table = 'CROSSTABLES'
        range = [year*100000, year*100000+99999]

        dbcsr = self._get_dbconn().cursor()
        sql = f'''
            select * from [{table}]
            where  [TOURN NUMBER] >= ? and [TOURN NUMBER] <= ?
            order by {sort}'''
        dbcsr.execute(sql, range)
        for row in dbcsr.fetchall():
            event = _mdb_to_event(row)
            result = _mdb_to_result(row)
            yield event, result
        dbcsr.close()


def _mdb_to_member(row):
    member = Member(
        cfc_id=_fmt_int(row, 'NUMBER'),
        cfc_expiry=_fmt_ymd(row, 'EXPIRY'),
        cfc_type=_fmt_code(row, 'TYPE'),
        fide_id=_fmt_int(row, 'FIDE NUMBER'),
        name_first=_fmt_str(row, 'FIRST'),
        name_last=_fmt_str(row, 'LAST'),
        gender=_fmt_code(row, 'SEX'),
        birthdate=_fmt_ymd(row, 'BIRTHDATE'),
        email=_fmt_str(row, 'Email'),
        addr_line1=_fmt_str(row, 'ADDRESS'),
        addr_city=_fmt_str(row, 'CITY'),
        addr_province=_fmt_code(row, 'PROV'),
        addr_postalcode=_fmt_code(row, 'POSTCODE'),
        regular_rating=_fmt_int(row, 'RATING'),
        regular_indicator=_fmt_int(row, 'INDICATOR'),
        quick_rating=_fmt_int(row, 'ACT_RATING'),
        quick_indicator=_fmt_int(row, 'ACT_INDIC'),
        notes=_fmt_str(row, 'Notes'),
        last_update=_fmt_ymd(row, 'Last Update'),
    )
    return member


def _mdb_to_event(row):
    event = Event(
        id=_fmt_int(row, 'TOURN NUMBER'),
        name= _fmt_str(row, 'TOURN NAME'),
        date_end=_fmt_ymd(row, 'FINISH DATE'),
        province=_fmt_code(row, 'PROVINCE'),
        arbiter_id=_fmt_int(row, 'TD NUMBER'),
        organizer_id=_fmt_int(row, 'ORG NUMBER'),
        pairings=_fmt_code(row, 'STYLE', {'S': 'SS', 'R': 'RR'}),
        rating_type=_fmt_code(row, 'TYPE', {'A': 'Q'}),
        n_players=_fmt_int(row, 'PLAYERS'),
        n_rounds=_fmt_int(row, 'ROUNDS'),
    )
    return event


def _mdb_to_result(row):
    result = EventResult(
        event_id=_fmt_int(row, 'TOURN NUMBER'),
        place=_fmt_int(row, 'FINISH POSITION'),
        cfc_id=_fmt_int(row, 'CFC NUMBER'),
        province=_fmt_code(row, 'PLAYERS PROV'),
        games_played=_fmt_int(row, 'GAMES PLAYED'),
        score=_fmt_int(row, 'TOTAL'),
        results=EventResult.normalize_results(getattr(row, 'RESULTS')),
        rating_type=_fmt_code(row, 'TYPE', {'A': 'Q'}),
        rating_pre=_fmt_int(row, 'PRE RATING'),
        rating_perf=_fmt_int(row, 'PERF RATING'),
        rating_post=_fmt_int(row, 'POST RATING'),
    )
    return result


# ----------------------------------------------------------------------
# Formatters: get from MS-Access row and format as necessary.
# ----------------------------------------------------------------------
def _fmt_int(row, attr):
    return int(getattr(row, attr) or 0)


def _fmt_str(row, attr):
    s = str(getattr(row, attr) or '')
    return s.strip()


def _fmt_ymd(row, attr):
    date = getattr(row, attr)
    return date.strftime('%Y-%m-%d') if date else ''


def _fmt_code(row, attr, convert=None):
    code = str(getattr(row, attr) or '').strip().upper()
    if convert and code in convert:
        code = convert[code]
    return code


# ======================================================================
# Schema of cfc*.mdb:
# - Table: "Membership Information":
#         BATCH                   Date With Time          8
#         SOURCE                  Short Text             10
#         NUMBER                  Double                  8
#         FIDE NUMBER             Long Integer            4
#         EXPIRY                  Date With Time          8
#         LAST EXPIRY             Date With Time          8
#         TYPE                    Short Text              1
#         GIFT                    Short Text              1
#         TD TYPE                 Long Integer            4
#         FIRST                   Short Text             50
#         LAST                    Short Text             50
#         ADDRESS                 Short Text             45
#         CITY                    Short Text             20
#         PROV                    Short Text              2
#         POSTCODE                Short Text              7
#         PHONE                   Double                  8
#         BIRTHDATE               Date With Time          8
#         RATING                  Integer                 2
#         INDICATOR               Integer                 2
#         SEX                     Short Text              1
#         SPECIAL                 Long Integer            4
#         ACT_RATING              Integer                 2
#         ACT_INDIC               Integer                 2
#         ACT_SPECIL              Long Integer            4
#         MISC                    Short Text              2
#         FIDE RATING             Long Integer            4
#         Account Receivable      Currency                8
#         Account Payable         Currency                8
#         Notes                   Long Text               -
#         CC Number               Short Text             16
#         CC Expiry               Date With Time          8
#         Auto Renew              Byte                    1
#         Email                   Short Text             50
#         Last Update             Date With Time          8
# ----------------------------------------------------------------------
# - Table: "CROSSTABLES":
#         TOURN NUMBER            Long Integer            4
#         FINISH POSITION         Integer                 2
#         CFC NUMBER              Double                  8
#         TOURN NAME              Short Text             35
#         FINISH DATE             Date With Time          8
#         REF NUMBER              Short Text              7
#         STYLE                   Short Text              3
#         TYPE                    Short Text              1
#         PROVINCE                Short Text              2
#         TD NUMBER               Long Integer            4
#         ORG NUMBER              Long Integer            4
#         PLAYERS                 Integer                 2
#         ROUNDS                  Integer                 2
#         GAMES PLAYED            Integer                 2
#         PRE RATING              Integer                 2
#         PERF RATING             Integer                 2
#         POST RATING             Integer                 2
#         RATING INDICATOR        Integer                 2
#         RESULTS                 Short Text            255
#         TOTAL                   Double                  8
#         PLAYERS PROV            Short Text              2
#         Last Update             Date With Time          8
#         ID                      Long Integer            4
