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
from ..models.member import Member
from ..models.event import Event
from ..models.event_result import EventResult


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
        table = 'CROSSTABLES'                   # Has [200601001; current++]
        # table = 'crosstables2000-2001'          # Has [200001033; 200012105]
        # table = 'CrosstablesBefore2000'         # Has [199607001; 200004004 + 200706020]
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
        phone=_fmt_str(row, 'PHONE'),
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
        score=_fmt_float(row, 'TOTAL'),
        results=EventResult.normalize_results(getattr(row, 'RESULTS'), getattr(row, 'TOURN NUMBER')),
        rating_type=_fmt_code(row, 'TYPE', {'A': 'Q'}),
        rating_pre=_fmt_int(row, 'PRE RATING'),
        rating_perf=_fmt_int(row, 'PERF RATING'),
        rating_post=_fmt_int(row, 'POST RATING'),
        rating_indicator=_fmt_int(row, 'RATING INDICATOR')
    )
    return result


# ----------------------------------------------------------------------
# Formatters: get from MS-Access row and format as necessary.
# ----------------------------------------------------------------------
def _fmt_int(row, attr):
    return int(getattr(row, attr) or 0)


def _fmt_float(row, attr):
    return float(getattr(row, attr) or 0)


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
# cfc*.mdb Schema:
# ======================================================================
# - Table: "Membership Information":
#         BATCH                   Date With Time          8     EXCLUDED
#         SOURCE                  Short Text             10     EXCLUDED
#         NUMBER                  Double                  8
#         FIDE NUMBER             Long Integer            4
#         EXPIRY                  Date With Time          8
#         LAST EXPIRY             Date With Time          8     EXCLUDED
#         TYPE                    Short Text              1
#         GIFT                    Short Text              1     EXCLUDED
#         TD TYPE                 Long Integer            4     EXCLUDED
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
#         SPECIAL                 Long Integer            4     EXCLUDED (id of last tournament)
#         ACT_RATING              Integer                 2
#         ACT_INDIC               Integer                 2
#         ACT_SPECIL              Long Integer            4     EXCLUDED
#         MISC                    Short Text              2     EXCLUDED (???: E, G, LG)
#         FIDE RATING             Long Integer            4     EXCLUDED (unreliable)
#         Account Receivable      Currency                8     EXCLUDED
#         Account Payable         Currency                8     EXCLUDED
#         Notes                   Long Text               -
#         CC Number               Short Text             16     EXCLUDED
#         CC Expiry               Date With Time          8     EXCLUDED
#         Auto Renew              Byte                    1     EXCLUDED
#         Email                   Short Text             50
#         Last Update             Date With Time          8

# ----------------------------------------------------------------------
# - Table: "CROSSTABLES":
#         TOURN NUMBER            Long Integer            4     Event, Result
#         FINISH POSITION         Integer                 2     Result
#         CFC NUMBER              Double                  8     Result
#         TOURN NAME              Short Text             35     Event
#         FINISH DATE             Date With Time          8     Event
#         REF NUMBER              Short Text              7     EXCLUDED (usually blank, 0, =TD NUMBER)
#         STYLE                   Short Text              3     Event (S=>SS, R=>RR)
#         TYPE                    Short Text              1     Event, Result (R, A=>Q)
#         PROVINCE                Short Text              2     Event
#         TD NUMBER               Long Integer            4     Event
#         ORG NUMBER              Long Integer            4     Event
#         PLAYERS                 Integer                 2     Event
#         ROUNDS                  Integer                 2     Event
#         GAMES PLAYED            Integer                 2     Result
#         PRE RATING              Integer                 2     Result
#         PERF RATING             Integer                 2     Result
#         POST RATING             Integer                 2     Result
#         RATING INDICATOR        Integer                 2     Result
#         RESULTS                 Short Text            255     Result
#         TOTAL                   Double                  8     Result
#         PLAYERS PROV            Short Text              2     Result
#         Last Update             Date With Time          8     EXCLUDED (MS-Access)
#         ID                      Long Integer            4     EXCLUDED (MS-Access row id)
