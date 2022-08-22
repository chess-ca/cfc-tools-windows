# ======================================================================
# services/cfc_mdb_update.py:
#   - Update a cfc*.mdb (MS-Access) with data from JustGo (MS-Excel)
#   - Ran weekly by Bob Gillanders just before the old Ratings program.
# ======================================================================
import logging, sys, pathlib, datetime
from .. import models as m
from . import utils

_console = logging.getLogger('console')
_OKAY = True


def update(members_xlsx, cfc_mdb, cfc_mdb_pw):
    now_dt = datetime.datetime.now()
    _console.info('%s: %s', now_dt.strftime('%Y-%m-%d-%H:%M:%S'), '-'*30)
    _console.info('Updating a CFC MS-Access database using CFC-Tools version %s', m.app.version)

    try:
        okay = _check_cfc_mdb_file(cfc_mdb)
        if okay:
            okay = _process_members(members_xlsx, cfc_mdb, cfc_mdb_pw)
    except:
        okay = not _OKAY
        excp = sys.exc_info()
        emsg = ('-'*64) + '\nEXCEPTION: %s\n%s\n' + ('-'*64)
        _console.error(emsg, excp[0], excp[1])

    if okay:
        _console.info('\nSUCCESS!  All updating completed')
    else:
        _console.info('\nFAILED!  Fix error and re-run')


# ======================================================================
def _check_cfc_mdb_file(cfc_mdb):
    _console.info('Updating %s', cfc_mdb)
    emsg = _is_file(cfc_mdb)
    if type(emsg) == str:
        _console.error(' - %s', emsg)
        return not _OKAY
    return _OKAY


# ======================================================================
def _process_members(members_xlsx, cfc_mdb, cfc_mdb_pw):
    ws_name = 'All Members'

    _console.info(f'Reading from "All Members With Custom Field" report:\n - File: {members_xlsx}')

    emsg = _is_file(members_xlsx)
    if type(emsg) == str:
        _console.error(f' - {emsg}')
        return not _OKAY

    mdb = utils.MDB(cfc_mdb, cfc_mdb_pw, 'Membership Information', 'NUMBER')
    n_read, n_added, n_updated = 0, 0, 0
    xlsx = utils.XLSX(members_xlsx, ws_name)

    cfc_added = []
    cfc_updated = []

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
            # ---- Set cols to defaults (MS-Access wasn't setting these correctly)
            ws_row['RATING'] = 0
            ws_row['INDICATOR'] = 0
            ws_row['ACT_RATING'] = 0
            ws_row['ACT_INDIC'] = 0
            mdb.insert(ws_row)
            cfc_added.append(str(int(ws_row['NUMBER'])))
        else:
            unequal_cols = _get_unequal_cols(mdb_row, ws_row)
            if len(unequal_cols) > 0:
                n_updated += 1
                # FOR DEBUGGING:
                # if n_updated > 100 and n_updated < 121:
                #     _console.info(f'   mid={ws_row["NUMBER"]}, cols={unequal_cols}')
                mdb.update(ws_row, unequal_cols)
                cfc_updated.append(str(int(ws_row['NUMBER'])))

        if n_read % 10000 == 0:
            _console.info(f'   ... {n_read:,} read; {n_updated:,} members updated; {n_added:,} members added')

    _console.info(f'   Finished: {n_read:,} read; {n_updated:,} members updated; {n_added:,} members added')
    _console.info(cfc_id_list(' - CFC ids added:', cfc_added))
    _console.info(cfc_id_list(' - CFC ids updated:', cfc_updated))
    return _OKAY


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
                continue
            if mdb_val and mdb_val > _dt_high and ws_val and ws_val > _dt_high:
                continue
        if ws_key == 'Email' and ws_val == '':
            continue    # Nothing new in the xlsx, so don't overwrite the old value.
        if mdb_val != ws_val:
            unequal_cols.append(ws_key)
    return unequal_cols


def cfc_id_list(line1, cfc_ids, per_row=10, indent=3):
    cfc_ids = sorted(cfc_ids)
    prefix = '\n' + (' ' * indent)
    out = line1
    if len(cfc_ids) == 0:
        out += prefix + '(none)'
    else:
        for i in range(0, len(cfc_ids), per_row):
            out += prefix + ', '.join(cfc_ids[i:i+per_row])
    return out
