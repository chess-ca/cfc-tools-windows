
from .. import models as m
from . import utils
import sys, pathlib, datetime, sqlite3, re

_sqlite_file = None

def create(cfc_mdb, cfc_mdb_pw):
    failed = False
    steps = [
        _check_cfc_mdb_file(cfc_mdb),
        _create_sqlite_tables(cfc_mdb),
        _extract_player_data(cfc_mdb, cfc_mdb_pw),
        _extract_tournament_data(cfc_mdb, cfc_mdb_pw),
        _create_sqlite_indices(cfc_mdb),
    ]
    try:
        for step in steps:
            if failed:
                break
            for msg in step:
                if msg is False:
                    failed = True
                    break
                else:
                    yield msg
    except:
        failed = True
        excp = sys.exc_info()
        emsg = f'{"-"*64}\nEXCEPTION: {excp[0]}\n'
        emsg += f'{excp[1]}\n{"-"*64}\n'
        yield emsg
    if failed:
        yield f'\nFAILED!  Fix error and re-run'
    else:
        yield f'\nSUCCESS!  Ratings database created'


# ======================================================================
def _check_cfc_mdb_file(cfc_mdb):
    ver = m.app.version
    yield f'Reading CFC database (with CFC-Tools {ver}):\n - File: {cfc_mdb}\n'
    emsg = _is_file(cfc_mdb)
    if type(emsg) == str:
        yield f' - {emsg}'
        yield False


# ======================================================================
def _create_sqlite_tables(cfc_mdb):
    global _sqlite_file
    yield f'Creating SQLite tables ...\n'

    # ---- SQLite
    _sqlite_file = pathlib.Path(cfc_mdb).with_suffix('.ratings.sqlite')
    if _sqlite_file.exists() and _sqlite_file.is_file():
        _sqlite_file.unlink()
    dbcon = sqlite3.connect(_sqlite_file)

    # ---- Table: metadata
    dbcon.execute('CREATE TABLE metadata (key text, value text)')
    sql = 'INSERT INTO metadata ("key", "value") VALUES (?, ?)'
    dbcon.execute(sql, ['created', datetime.date.today().isoformat()])

    # ---- Table: player
    cols = [
        'm_id number', 'fide_id number', 'expiry text',
        'first text', 'last text', 'first_lc text', 'last_lc text',
        'city text', 'prov text',
        'sex text', 'birthdate text',
        'rating number', 'rating_hi number', 'quick number', 'quick_hi number',
    ]
    sql = 'CREATE TABLE player (' + ', '.join(cols) + ')'
    dbcon.execute(sql)

    # ---- Table: tournament
    cols = [
        't_id number', 'name text', 'last_day text', 'prov text',
        'rounds number', 'pairings text', 'type text', 'org_m_id number',
    ]
    sql = 'CREATE TABLE tournament (' + ', '.join(cols) + ')'
    dbcon.execute(sql)

    # ---- Table: crosstable
    cols = [
        # ????: "RANK_ID"
        't_id number', 'place number', 'm_id number',
        'results text', 'score number', 'games_played number',
        'rating_pre number', 'rating_perf number', 'rating_post number',
        'rating_hi number',
    ]
    sql = 'CREATE TABLE crosstable (' + ', '.join(cols) + ')'
    dbcon.execute(sql)

    dbcon.commit()
    dbcon.close()
    yield f'   SQLite tables created.\n'


# ======================================================================
def _create_sqlite_indices(cfc_mdb):
    yield f'Creating SQLite indices ...\n'

    if not _sqlite_file:
        yield f'    ERROR: SQLite file not defined'
        yield False
        return
    dbcon = sqlite3.connect(_sqlite_file)
    dbcon.execute('CREATE INDEX ix_player_1 ON player (m_id)')
    dbcon.execute('CREATE INDEX ix_player_2 ON player (last_lc, first_lc)')
    dbcon.execute('CREATE INDEX ix_tournament_1 ON tournament (t_id)')
    dbcon.execute('CREATE INDEX ix_crosstable_1 ON crosstable (t_id, place)')
    dbcon.execute('CREATE INDEX ix_crosstable_2 ON crosstable (m_id)')
    dbcon.commit()
    dbcon.close()
    yield f'   SQLite indices created.\n'


# ======================================================================
def _extract_player_data(cfc_mdb, cfc_mdb_pw):
    yield f'Copying player data into the SQLite database ...\n'
    n_read, n_added = 0, 0
    if not _sqlite_file:
        yield f'    ERROR: SQLite file not defined'
        yield False
        return

    dbcon = sqlite3.connect(_sqlite_file)
    mdb = utils.MDB(cfc_mdb, cfc_mdb_pw, 'Membership Information', 'NUMBER')
    for row in mdb.get_all():
        n_read += 1
        v_expiry = getattr(row, 'EXPIRY')
        v_expiry = '' if not v_expiry else v_expiry.strftime('%Y-%m-%d')
        v_birth = getattr(row, 'BIRTHDATE')
        v_birth = '' if not v_birth else v_birth.strftime('%Y-%m-%d')
        sqldata = dict(
            m_id=getattr(row, 'NUMBER'),
            fide_id=getattr(row, 'FIDE NUMBER'),
            expiry=v_expiry,
            first=getattr(row, 'FIRST'),
            last=getattr(row, 'LAST'),
            first_lc=str(getattr(row, 'FIRST')).lower(),
            last_lc=str(getattr(row, 'LAST')).lower(),
            city=getattr(row, 'CITY'),
            prov=getattr(row, 'PROV'),
            sex=getattr(row, 'SEX'),
            birthdate=v_birth,
            rating=getattr(row, 'RATING'),
            rating_hi=getattr(row, 'INDICATOR'),
            quick=getattr(row, 'ACT_RATING'),
            quick_hi=getattr(row, 'ACT_INDIC'),
        )
        keys = sqldata.keys()
        sql = 'INSERT INTO player (' + ', '.join(keys) \
            + ') VALUES (' + ','.join(['?' for k in keys]) + ')'
        dbcon.execute(sql, [sqldata[k] for k in keys])
        n_added += 1
        if n_added % 1000 == 0:
            dbcon.commit()
        if n_added % 25000 == 0:
            yield f'   ... added {n_added:,}'

    dbcon.commit()
    dbcon.close()
    yield f'   Finished: {n_added:,} players added\n'


# ======================================================================
def _extract_tournament_data(cfc_mdb, cfc_mdb_pw):
    yield f'Copying tournament data into the SQLite database ...\n'
    n_read, n_tournaments, n_crosstables = 0, 0, 0
    if not _sqlite_file:
        yield f'    ERROR: SQLite file not defined'
        yield False
        return

    re_spaces = re.compile(r'\s+')
    dbcon = sqlite3.connect(_sqlite_file)
    mdb = utils.MDB(cfc_mdb, cfc_mdb_pw, 'CROSSTABLES', 'TOURN NUMBER')
    previous_tid = -1
    for row in mdb.get_all(sort='"TOURN NUMBER", "FINISH POSITION"'):
        n_read += 1
        v_tid = getattr(row, 'TOURN NUMBER')
        if v_tid != previous_tid:
            v_pairings = getattr(row, 'STYLE')
            v_pairings = 'SS' if v_pairings == 'S' \
                else 'RR' if v_pairings == 'R' \
                else v_pairings
            v_type = getattr(row, 'TYPE')
            v_type = 'Q' if v_type == 'A' \
                else v_type
            v_last_day = getattr(row, 'FINISH DATE')
            v_last_day = '' if not v_last_day else v_last_day.strftime('%Y-%m-%d')
            sqldata = dict(
                t_id=v_tid,
                name=getattr(row, 'TOURN NAME'),
                last_day=v_last_day,
                prov=getattr(row, 'PROVINCE'),
                rounds=getattr(row, 'ROUNDS'),
                pairings=v_pairings,
                type=v_type,
                org_m_id=getattr(row, 'ORG NUMBER'),
            )
            keys = sqldata.keys()
            sql = 'INSERT INTO tournament (' + ', '.join(keys) \
                  + ') VALUES (' + ','.join(['?' for k in keys]) + ')'
            dbcon.execute(sql, [sqldata[k] for k in keys])
            n_tournaments += 1
            previous_tid = v_tid

        v_results = getattr(row, 'RESULTS', '').strip().upper()
        if 'X' in v_results:
            v_results = '|'.join([c for c in v_results])
        else:
            v_results = re_spaces.sub('|', v_results)
        sqldata = dict(
            t_id=v_tid,
            place=getattr(row, 'FINISH POSITION'),
            m_id=getattr(row, 'CFC NUMBER'),
            results=v_results,
            score=getattr(row, 'TOTAL'),
            games_played=getattr(row, 'GAMES PLAYED'),
            rating_pre=getattr(row, 'PRE RATING'),
            rating_perf=getattr(row, 'PERF RATING'),
            rating_post=getattr(row, 'POST RATING'),
            rating_hi=getattr(row, 'RATING INDICATOR'),
        )
        keys = sqldata.keys()
        sql = 'INSERT INTO crosstable (' + ', '.join(keys) \
              + ') VALUES (' + ','.join(['?' for k in keys]) + ')'
        dbcon.execute(sql, [sqldata[k] for k in keys])
        n_crosstables += 1
        if n_crosstables % 1000 == 0:
            dbcon.commit()
        if n_crosstables % 50000 == 0:
            yield f'   ... added {n_crosstables:,}'

    dbcon.commit()
    dbcon.close()
    yield f'   Finished: {n_crosstables:,} player results and {n_tournaments:,} tournaments added\n'


# ======================================================================
def _process_members(members_xlsx, cfc_mdb, cfc_mdb_pw):
    ws_name = 'All Members'

    yield f'Reading from "All Members With Custom Field" report:\n - File: {members_xlsx}\n'

    emsg = _is_file(members_xlsx)
    if type(emsg) == str:
        yield f' - {emsg}'
        yield False
        return

    mdb = utils.MDB(cfc_mdb, cfc_mdb_pw, 'Membership Information', 'NUMBER')
    n_read, n_added, n_updated = 0, 0, 0
    xlsx = utils.XLSX(members_xlsx, ws_name)

    for ws_row in xlsx.get_all():
        n_read += 1
        # if n_read < 10123:
        #     continue
        # if n_read > 10126:
        #     break

        ws_row = _to_mdb_format(members_row=ws_row)
        if ws_row['NUMBER'] is None:
            continue        # an empty row in the spreadsheet
        if int(ws_row['NUMBER']) < 100000:
            continue        # a dummy CFC id

        mdb_row = mdb.get_id(ws_row['NUMBER'])
        if mdb_row is None:
            n_added += 1
            mdb.insert(ws_row)
            continue

        unequal_cols = _get_unequal_cols(mdb_row, ws_row)
        if len(unequal_cols) > 0:
            n_updated += 1
            # FOR DEBUGGING:
            # if n_updated > 100 and n_updated < 121:
            #     yield f'   mid={ws_row["NUMBER"]}, cols={unequal_cols}'
            mdb.update(ws_row, unequal_cols)
        if n_read % 10000 == 0:
            yield f'   ... {n_read:,} read; {n_updated:,} members updated; {n_added} members added\n'
    yield f'   Finished: {n_read} read; {n_updated:,} members updated; {n_added} members added\n'


# ======================================================================
# Shared Functions
# ======================================================================
def _is_file(filename):
    if not filename:
        return f'Error: File not specified\n'
    fp = pathlib.Path(filename)
    if not fp.exists():
        return f'Error: File not found: {filename}\n'
    if not fp.is_file():
        return f'Error: Must be a file: {filename}\n'
    return True


def _to_mdb_format(members_row=None, fields_row=None):
    # Note: MS-Access has a "Allow zero length" property for text fields.
    #   In cfc.mdb, most text fields do not "allow zero length" which
    #   means attempting to set to "" (zero length) causes an error.
    mdb = {}
    if members_row:
        # Has: MID, First Name, Last Name, Email Address, Date of Birth, Gender,
        #       Address Line 1, Address Line 2, Town, County, Postcode, Country,
        #       Member State, Membership Type, Membership Expiry, Membership State,
        #       FIDE Membership Id, Provincial Affiliation
        r = members_row
        mdb['NUMBER'] = _fmt_val(r['MID'], type=float)                # float
        mdb['FIRST'] = _fmt_val(r['First Name'], type=str)
        mdb['LAST'] = _fmt_val(r['Last Name'], type=str)
        g = _fmt_val(r['Gender'], type=str).upper()
        # Note: .mdb requires None or non-zero length string
        mdb['SEX'] = 'M' if g == 'MALE' else 'F' if g == 'FEMALE' else None
        mdb['ADDRESS'] = _fmt_val(r['Address Line 1'], type=str)
        aline2 = _fmt_val(r['Address Line 2'], type=str)
        if aline2 != ' ':
            mdb['ADDRESS'] = f'; {aline2}'
        mdb['CITY'] = _fmt_val(r['Town'], type=str)
        mdb['PROV'] = utils._province_to_pp(r['County'])
        mdb['BIRTHDATE'] = r['Date of Birth']               # datetime
        mdb['EXPIRY'] = r['Membership Expiry']              # datetime
        mdb['Email'] = _fmt_val(r['Email Address'], type=str)
        mdb['POSTCODE'] = _fmt_val(r['Postcode'], type=str)
        mdb['FIDE NUMBER'] = _fmt_val(r['FIDE Membership Id'], type=float)
    elif fields_row:
        # REMOVED: no longer using the membership fields report/.xlsx
        pass
    return mdb


def _fmt_val(val, type=None):
    if type == str:
        if val is None:
            val = ' '
        val = str(val).strip()
        if val == '':       # In cfc.mdb, text fields have "Allow zero length" set to "no".
            val = ' '
    elif type == float:
        try:
            val = str(val or '').strip()
            val = float(val)
        except:
            val = None
    return val


_dt_high = datetime.datetime(2080, 1, 1)
_dt_low = datetime.datetime(1961, 12, 31)
def _get_unequal_cols(mdb_row, ws_row):
    unequal_cols = []
    for ws_key, ws_val in ws_row.items():
        if type(ws_val) == str:
            ws_val = ws_val.strip()
        mdb_val = getattr(mdb_row, ws_key, None)
        if type(mdb_val) == str:
            mdb_val = mdb_val.strip()
        if (mdb_val is None or mdb_val == '') and (ws_val is None or ws_val == ''):
            continue    # None and '' does not require updating
        if ws_key == 'EXPIRY':
            if not ws_val:
                continue    # Nothing new in the xlsx, so don't overwrite the old value.
            if mdb_val and mdb_val < _dt_low and ws_val and ws_val < _dt_low:
                continue    # < LOW_VALUE so probably indicating something (not a real date)
            if mdb_val and mdb_val > _dt_high and ws_val and ws_val > _dt_high:
                continue    # > HIGH_VALUE so probably a LIFE member
        if ws_key == 'Email' and ws_val == '':
            continue    # Nothing new in the xlsx, so don't overwrite the old value.
        if mdb_val != ws_val:
            unequal_cols.append(ws_key)
    return unequal_cols
