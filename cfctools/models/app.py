
from types import SimpleNamespace
import pathlib


class App(SimpleNamespace):
    version = '1.2.0'
    title = 'CFC Tools'
    dir_root = pathlib.Path(__file__).parents[2]

    # ---- Global access (initialized by Application, etc)
    instance = None
    window_main = None


app = App()
