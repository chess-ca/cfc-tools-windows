
import argparse

def args_parse():
    ap = argparse.ArgumentParser(description='CFC Tools for Business Office tasks')
    ap.add_argument('-a', '--action', dest='action',
                    help='run action via command line (not via graphical user interface)')
    return ap.parse_args()
