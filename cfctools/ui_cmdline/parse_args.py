
import argparse

def parse_args():
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
    ap.add_argument('--drupal', dest='drupal_csv',
                    help='CSV file extracted from Drupal\'s database')
    return ap.parse_args()
