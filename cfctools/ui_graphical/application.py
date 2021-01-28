
from typing import Callable
from . import main, cfc_mdb_extract, cfc_mdb_update


class Application():
    w_singleton = None

    def __init__(self):
        self.__class__.w_singleton = self

    def quit(self):
        Routes.QUIT()

    def run(self, args=None):
        main.MainWindow.create_singleton().mainloop()


# ---- Routing to Pages, etc. Used by Tk widgets in command=<callable-route>
class Routes:
    HOME: Callable = main.HomePage.show
    QUIT: Callable = main.MainWindow.exit_window
    HELP: Callable = main.UnderConstructionPage.show
    CFC_MDB_UPDATE_ARGS: Callable = cfc_mdb_update.GetArgsPage.show
    CFC_MDB_UPDATE_RUN: Callable = cfc_mdb_update.RunPage.show
    CFC_MDB_EXTRACT_ARGS: Callable = cfc_mdb_extract.GetArgsPage.show
    CFC_MDB_EXTRACT_RUN: Callable = cfc_mdb_extract.RunPage.show
    UNDER_CONSTRUCTION: Callable = main.UnderConstructionPage.show


def update_gui():
    mw = main.MainWindow.get_singleton()
    mw.update()
