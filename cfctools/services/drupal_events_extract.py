
import os, sys, io, pathlib, logging, datetime, re
from .. import models as m
from ..models.member import Member
from ..models.event import Event
from ..models.event_result import EventResult
from ..datamappers.job import JobFile
from ..datamappers.drupal import DrupalCsv
# from ..datamappers.cfcmdb import CfcMdb
from ..datamappers.csv import CsvInMemory

_console = logging.getLogger('console')
_OKAY = True


def extract(drupal_csv, updated_text=None):
    updated_text = updated_text or datetime.datetime.now().strftime('%Y-%m-%d')
    _console.info('Extracting from Drupal CSV using CFC-Tools version %s', m.app.version)
    jobfile = None

    try:
        okay = _check_drupal_csv(drupal_csv)
        if okay:
            okay, jobfile = _create_jobfile(drupal_csv, updated_text)
        if okay:
            okay = _extract_events(jobfile, drupal_csv)
        _close_jobfile(jobfile)
    except:
        okay = not _OKAY
        excp = sys.exc_info()
        emsg = ('-'*64) + '\nEXCEPTION: %s\n%s\n' + ('-'*64)
        _console.error(emsg, excp[0], excp[1])

    if okay:
        _console.info('\nSUCCESS!  JobFile created')
    else:
        _console.info('\nFAILED!  Fix error and re-run')


# ======================================================================
def _check_drupal_csv(drupal_csv):
    _console.info('Extracting from %s', drupal_csv)
    error_msg = _is_file(drupal_csv)
    if isinstance(error_msg, str):
        _console.error(' - %s', error_msg)
        return not _OKAY
    return _OKAY


# ======================================================================
def _create_jobfile(drupal_csv, updated_text):
    mdp_path = pathlib.Path(drupal_csv)
    jobfile_path = mdp_path.with_suffix('.from-drupal.job.zip')
    jobfile = JobFile(
        jobfile_path, mode='w',
        title='Extract from Drupal CSV: ' + mdp_path.name,
        handler='drupal-events-extract',
        args={
            'api-version': '1.0',
            'updated_text': updated_text,
        },
    )
    jobfile.comment(f'JobFile created by "{os.getlogin()}" on "{sys.platform}"')
    _console.info('   JobFile opened: %s', jobfile_path)
    return _OKAY, jobfile


# ======================================================================
def _close_jobfile(jobfile):
    fname = jobfile.get_filename()
    if callable(getattr(jobfile, 'close', None)):
        jobfile.close()
    _console.info('JobFile created: %s', fname)
    return _OKAY


# ======================================================================
def _extract_events(jobfile, drupal_csv):
    _console.info('Extracting events ...')
    for year in range(1996, 2020+1):
        csv_events, csv_results = _extract_events_for_year(year, drupal_csv)
        _console.info('   ... For year %d, found %d events.', year, len(csv_events))
        csv_events.flush_to_zipfile(f'ratings.{year}.events.from-drupal.csv', jobfile)
        csv_results.flush_to_zipfile(f'ratings.{year}.results.from-drupal.csv', jobfile)
    return _OKAY


def _extract_events_for_year(year, drupal_csv):
    id_min = year * 100000
    id_max = id_min + 99999
    events_list = {}
    for event, results in DrupalCsv(drupal_csv).fetch_event_results():
        if event.id < id_min or event.id > id_max:
            continue
        if event.id not in events_list:
            event.n_players = 0
            events_list[event.id] = (event, [],)
        events_list[event.id][0].n_players += 1
        events_list[event.id][1].append(results)

    csv_events = CsvInMemory(Event)
    csv_results = CsvInMemory(EventResult)
    for id in sorted(events_list.keys()):
        event, results_list = events_list[id]
        csv_events.writerow(event)
        results_list = sorted(results_list, key=lambda er: er.place)
        for er in results_list:
            csv_results.writerow(er)

    return csv_events, csv_results




# def _extract_events_for_year(year, jobfile, cfc_mdb, cfc_mdb_pw):
#     n_events = 0
#     previous_event_id = None
#     csv_events = CsvInMemory(Event)
#     csv_results = CsvInMemory(EventResult)
#
#     with CfcMdb(cfc_mdb, cfc_mdb_pw) as mdb:
#         for event, result in mdb.fetch_events_for_year(year):
#             if event.id != previous_event_id:
#                 n_events += 1
#                 csv_events.writerow(event)
#                 previous_event_id = event.id
#             csv_results.writerow(result)
#
#     csv_events.flush_to_zipfile(f'{year}.events.from-drupal.csv', jobfile)
#     csv_results.flush_to_zipfile(f'{year}.event-results.from-drupal.csv', jobfile)
#     if n_events > 0:
#         _console.info(f'   ... For {year}, extracted {n_events:,} events.')
#     return n_events


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


# def _to_mdb_format(members_row=None, fields_row=None):
#     # Note: MS-Access has a "Allow zero length" property for text fields.
#     #   In cfc.mdb, most text fields do not "allow zero length" which
#     #   means attempting to set to "" (zero length) causes an error.
#     mdb = {}
#     if members_row:
#         # Has: MID, First Name, Last Name, Email Address, Date of Birth, Gender,
#         #       Address Line 1, Address Line 2, Town, County, Postcode, Country,
#         #       Member State, Membership Type, Membership Expiry, Membership State,
#         #       FIDE Membership Id, Provincial Affiliation
#         r = members_row
#         mdb['NUMBER'] = _fmt_val(r['MID'], type=float)                # float
#         mdb['FIRST'] = _fmt_val(r['First Name'], type=str)
#         mdb['LAST'] = _fmt_val(r['Last Name'], type=str)
#         g = _fmt_val(r['Gender'], type=str).upper()
#         # Note: .mdb requires None or non-zero length string
#         mdb['SEX'] = 'M' if g == 'MALE' else 'F' if g == 'FEMALE' else None
#         mdb['ADDRESS'] = _fmt_val(r['Address Line 1'], type=str)
#         aline2 = _fmt_val(r['Address Line 2'], type=str)
#         if aline2 != ' ':
#             mdb['ADDRESS'] = f'; {aline2}'
#         mdb['CITY'] = _fmt_val(r['Town'], type=str)
#         mdb['PROV'] = utils._province_to_pp(r['County'])
#         mdb['BIRTHDATE'] = r['Date of Birth']               # datetime
#         mdb['EXPIRY'] = r['Membership Expiry']              # datetime
#         mdb['Email'] = _fmt_val(r['Email Address'], type=str)
#         mdb['POSTCODE'] = _fmt_val(r['Postcode'], type=str)
#         mdb['FIDE NUMBER'] = _fmt_val(r['FIDE Membership Id'], type=float)
#     elif fields_row:
#         # REMOVED: no longer using the membership fields report/.xlsx
#         pass
#     return mdb


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
