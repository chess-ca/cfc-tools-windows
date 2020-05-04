
from .. import models as m
from . import utils
import sys, pathlib, datetime


def update(members_xlsx, fields_xlsx, cfc_mdb, cfc_mdb_pw):
    failed = False
    steps = [_check_cfc_mdb_file(cfc_mdb)]
    if members_xlsx.strip() != '':
        steps.append(_process_members(members_xlsx, cfc_mdb, cfc_mdb_pw))
    if fields_xlsx.strip() != '':
        steps.append(_process_fields(fields_xlsx, cfc_mdb, cfc_mdb_pw))
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
        yield f'\nSUCCESS!  All updating completed'


# ======================================================================
def _check_cfc_mdb_file(cfc_mdb):
    ver = m.app.version
    yield f'Updating CFC database (with CFC-Tools {ver}):\n - File: {cfc_mdb}\n'
    emsg = _is_file(cfc_mdb)
    if type(emsg) == str:
        yield f' - {emsg}'
        yield False


# ======================================================================
def _process_members(members_xlsx, cfc_mdb, cfc_mdb_pw):
    ws_name = 'Data'

    yield f'Reading from "All Members" report:\n - File: {members_xlsx}\n'

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
            mdb.update(ws_row, unequal_cols)
        if n_read % 10000 == 0:
            yield f'   ... {n_read:,} read; {n_updated:,} members updated; {n_added} members added\n'
    yield f'   Finished: {n_read} read; {n_updated:,} members updated; {n_added} members added\n'


# ======================================================================
def _process_fields(fields_xlsx, cfc_mdb, cfc_mdb_pw):
    ws_name = 'FieldEditor_NGB'

    yield f'Reading "Members and Fields (NGB)" report:\n - File: {fields_xlsx}\n'

    emsg = _is_file(fields_xlsx)
    if type(emsg) == str:
        yield f' - {emsg}'
        yield False
        return

    mdb = utils.MDB(cfc_mdb, cfc_mdb_pw, 'Membership Information', 'NUMBER')
    n_read, n_updated = 0, 0
    xlsx = utils.XLSX(fields_xlsx, ws_name)

    for ws_row in xlsx.get_all():
        n_read += 1
        # if n_read < 10123:
        #     continue
        # if n_read > 10126:
        #     break

        ws_row = _to_mdb_format(fields_row=ws_row)
        if ws_row['NUMBER'] is None:
            continue        # an empty row in the spreadsheet
        if int(ws_row['NUMBER']) < 100000:
            continue        # a dummy CFC id

        mdb_row = mdb.get_id(ws_row['NUMBER'])
        if mdb_row is None:
            continue        # cannot add member since only have minimal info

        unequal_cols = _get_unequal_cols(mdb_row, ws_row)
        if len(unequal_cols) > 0:
            n_updated += 1
            mdb.update(ws_row, unequal_cols)
        if n_read % 10000 == 0:
            yield f'   ... {n_read:,} read; {n_updated:,} members updated\n'
    yield f'   Finished: {n_read} read; {n_updated:,} members updated\n'


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
        #       Member State, Membership, Membership Expiry, Primary Club, Additional Clubs
        r = members_row
        mdb['NUMBER'] = _fmt_val(r['MID'], type=float)                # float
        mdb['FIRST'] = _fmt_val(r['First Name'], type=str)
        mdb['LAST'] = _fmt_val(r['Last Name'], type=str)
        g = _fmt_val(r['Gender'], type=str)
        # Note: .mdb requires None or non-zero length string
        mdb['SEX'] = 'M' if g == 'Male' else 'F' if g == 'Female' else None
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
    elif fields_row:
        # Has: MID, Firstname, Lastname, Category, Expiry,
        #       Additional Info - FIDE Membership Id, Additional Info - Provincial Affiliation
        r = fields_row
        mdb['NUMBER'] = _fmt_val(r['MID'], type=float)                # float
        mdb['FIDE NUMBER'] = _fmt_val(r['Additional Info - FIDE Membership Id'], type=float)
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
