
from types import SimpleNamespace
import pathlib


class App(SimpleNamespace):
    version = '2.0.0'
    title = 'CFC Tools'
    dir_root = pathlib.Path(__file__).parents[2]

    # ---- Global access (initialized by Application, etc)
    instance = None
    window_main = None

    # ---- Colours
    c_header_bg = '#a6be8e'
    c_off_white = '#fefbf6'
    c_text = '#404040'


app = App()
