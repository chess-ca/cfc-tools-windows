
import argparse

def args_parse():
    ap = argparse.ArgumentParser(description='CFC Tools for Business Office tasks')
    ap.add_argument('-a', '--action', dest='action',
                    help='run action via command line (not via graphical user interface)')
    ap.add_argument('--cmum', dest='cmu_members',
        help='"All Members With Custom Field" report (an .xlsx file)')
    ap.add_argument('--cmuc', dest='cmu_cfcmdb',
        help='"cfc*.mdb" database to be updated (an .mdb file)')
    ap.add_argument('--cmupw', dest='cmu_cfcmdb_pw',
        help='Password for the "cfc*.mdb" database')
    return ap.parse_args()
