
import csv, datetime
from ..models.event import Event
from ..models.event_result import EventResult


class DrupalCsv:
    def __init__(self, file):
        self.file = file

    def fetch_event_results(self):
        with open(self.file, newline='') as file_obj:
            csv_in = csv.DictReader(file_obj)
            for row in csv_in:
                event = _csv_to_event(row)
                result = _csv_to_result(row)
                yield event, result


def _csv_to_event(row):
    event = Event(
        id=_fmt_int(row, 'tournamentID'),
        name= _fmt_str(row, 'tournament_name'),
        date_end=_fmt_ymd(row, 'finish_date'),
        province=_fmt_code(row, 'province'),
        arbiter_id=_fmt_int(row, 'td_number'),
        organizer_id=0,     # _fmt_int(row, 'ORG NUMBER'),
        pairings=_fmt_code(row, 'style', {'S': 'SS', 'R': 'RR'}),
        rating_type=_fmt_code(row, 'type', {'A': 'Q'}),
        n_players=-1,       # _fmt_int(row, 'PLAYERS'),
        n_rounds=_fmt_int(row, 'rounds'),
    )
    return event


def _csv_to_result(row):
    result = EventResult(
        event_id=_fmt_int(row, 'tournamentID'),
        place=_fmt_int(row, 'finish_position'),
        cfc_id=_fmt_int(row, 'memberID'),
        province='',    # _fmt_code(row, 'PLAYERS PROV'),
        games_played=_fmt_int(row, 'games_played'),
        score=_fmt_float(row, 'total'),
        results=EventResult.normalize_results(row.get('results'), row.get('tournamentID')),
        rating_type=_fmt_code(row, 'type', {'A': 'Q'}),
        rating_pre=_fmt_int(row, 'pre_rating'),
        rating_perf=_fmt_int(row, 'perf_rating'),
        rating_post=_fmt_int(row, 'post_rating'),
        rating_indicator=_fmt_int(row, 'rating_indicator')
    )
    return result


# ----------------------------------------------------------------------
# Formatters: get from MS-Access row and format as necessary.
# ----------------------------------------------------------------------
def _fmt_int(row, attr):
    return int(row.get(attr) or 0)


def _fmt_float(row, attr):
    return float(row.get(attr) or 0)


def _fmt_str(row, attr):
    s = str(row.get(attr) or '')
    return s.strip()


def _fmt_ymd(row, attr):
    date = row.get(attr)
    if isinstance(date, datetime.datetime):
        date = date.strftime('%Y-%m-%d')
    return date or ''


def _fmt_code(row, attr, convert=None):
    code = str(row.get(attr) or '').strip().upper()
    if convert and code in convert:
        code = convert[code]
    return code

# ======================================================================
# Drupal Schema:
# - Drupal data was required because the CFC MS-Access databases no
#   longer had Event/Result data for 2001-2005 (but Drupal did)
# - Drupal data was not used for all 1996-2018 Event/Results data
#   because Drupal was missing "ORG NUMBER", "RATING INDICATOR",
#   and "PLAYERS PROV". Not essential but still nice not to lose.
# ======================================================================
# - Table: cfc_member_rankings      Database: chess_ca_ratings
#   - itemID                    EXCLUDED (???: "8105_1996")
#   - memberID                  Result
#   - tournamentID              Event, Result
#   - tournament_name           Event
#   - finish_date               Event
#   - province                  Event
#   - style                     Event (S=>SS; R=>RR)
#   - td_number                 Event
#   - finish_position           Result
#   - pre_rating                Result
#   - perf_rating               Result
#   - post_rating               Result
#   - results                   Result
#   - games_played              Result
#   - type                      Event, Result (R, A=>Q)
#   - rounds                    Event
#   - total                     Result
#   - rating_indicator          Result
