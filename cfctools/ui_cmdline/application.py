# ======================================================================
# Class Application:
# - For invoking the application from the command line.
# ======================================================================
import logging, argparse
from .. import services

_console = logging.getLogger('console')
_console.addHandler(logging.StreamHandler())
_console.setLevel(logging.INFO)


class Application:
    def run(self, args=None):
        if args.action == 'cmu':
            from ..services import cfc_mdb_update
            cfc_mdb_update.update(args.cmu_members, args.cmu_cfcmdb, args.cmu_cfcmdb_pw)
        elif args.action == 'r':
            _ratings_database_create(args)
        elif args.action == 'emdb':
            from ..services import extract_from_mdb
            extract_from_mdb.extract(args.cmu_cfcmdb, args.cmu_cfcmdb_pw)
        else:
            print(f'Unknown action: "{args.action}"')


def _ratings_database_create(args):
    ratings_args = dict(
        cfc_mdb=args.cmu_cfcmdb,
        cfc_mdb_pw=args.cmu_cfcmdb_pw,
    )
    for stdout in services.ratings_database_create.create(**ratings_args):
        print(stdout[0:-1] if stdout[-1:] == '\n' else stdout)


def _parse_args():
    ap = argparse.ArgumentParser(description='CFC Tools for Business Office tasks')
    # --- Action to perform (if not specified, invoke graphical UI)
    ap.add_argument('-a', '--action', dest='action',
                    help='"cmu" for CFC Members Update (GoMembership data); "r" for Ratings Database create')
    # --- CFC Members Update (cmu) with GoMembership data
    ap.add_argument('--cmum', dest='cmu_members',
                    help='"All Members With Custom Field" report (an .xlsx file)')
    ap.add_argument('--cmuc', dest='cmu_cfcmdb',
                    help='"cfc*.mdb" database to be updated (an .mdb file)')
    ap.add_argument('--cmupw', dest='cmu_cfcmdb_pw',
                    help='Password for the "cfc*.mdb" database')
    return ap.parse_args()

