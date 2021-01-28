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
            cfc_mdb_update.update(
                args.cmu_members,
                args.cmu_cfcmdb,
                args.cmu_cfcmdb_pw
            )
        elif args.action == 'r':
            from ..services import ratings_database_create
            ratings_database_create.create(
                cfc_mdb=args.cmu_cfcmdb,
                cfc_mdb_pw=args.cmu_cfcmdb_pw,
            )
        elif args.action == 'emdb':
            from ..services import extract_from_mdb
            extract_from_mdb.extract(
                args.cmu_cfcmdb,
                args.cmu_cfcmdb_pw
            )
        else:
            print(f'Unknown action: "{args.action}"')
