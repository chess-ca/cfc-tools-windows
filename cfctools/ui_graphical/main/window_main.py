# ======================================================================
# window_main.py:
# - The GUI's main window with common header, main-menu, body, footer.
# ======================================================================
import tkinter as tk
from tkinter import ttk
import cfctools.ui_graphical.application as app
from ..main import app_widgets, app_style
from .. import main, cfc_mdb_extract, cfc_mdb_update
from ... import models as m


class MainWindow(app_widgets.Window):
    def init_widget(self, **kwargs):
        self.configure(bg=app_style.c_bg,)
        self.minsize(width=800, height=600)
        app_style.init_style(main_tk=self)

        self.title(m.app.title)
        self.config(menu=_MainWindowsMenu(parent=self))

        _WindowHead(self).pack(fill=tk.X)
        _WindowBody(self).pack(fill=tk.BOTH, expand=True)
        _WindowFoot(self).pack(fill=tk.X)


class _WindowHead(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='WindowHead.TFrame')

        ttk.Label(self, style='WindowHead.TLabel',
            text=m.app.title,
            padding=(16,16,16,16,),
        ).pack(anchor=tk.W)


class _WindowBody(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # ---- Initialize each section of the app. Will create the child widgets (Pages)
        main.init_pages(parent=self)
        cfc_mdb_extract.init_pages(parent=self)
        cfc_mdb_update.init_pages(parent=self)
        app.Routes.HOME()


class _WindowFoot(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self,
            text=f'Version: {m.app.version}',
        ).pack(anchor=tk.E, padx=8, pady=2,)


class _MainWindowsMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self._menu_style = app_style.TK_MENU()
        self.config(**self._menu_style)
        self._add_File_submenu()
        self._add_Tools_submenu()
        self._add_Help_submenu()

    def _add_File_submenu(self):
        menu_1 = tk.Menu(self, tearoff=False, **self._menu_style)
        menu_1.add_command(
            label="Exit",
            command=app.Routes.QUIT,
            # accelerator='Ctrl+W'
        )
        self.add_cascade(label='File', menu=menu_1)

    def _add_Tools_submenu(self):
        menu_1 = tk.Menu(self, tearoff=False, **self._menu_style)
        menu_1.add_command(
            label='Home',
            command=app.Routes.HOME,
        )
        menu_1.add_separator()
        menu_1.add_command(
            label='Update cfc.mdb ...',
            command=app.Routes.CFC_MDB_UPDATE_ARGS,
        )
        menu_1.add_command(
            label='Extract from cfc.mdb ...',
            command=app.Routes.CFC_MDB_EXTRACT_ARGS,
        )
        self.add_cascade(label='Tools', menu=menu_1)

    def _add_Help_submenu(self):
        menu_1 = tk.Menu(self, tearoff=False, **self._menu_style)
        # menu_1.add_command(
        #     label='Update cfc.mdb',
        #     #command=self.callbacks['file->quit'],
        # )
        self.add_cascade(label='Help', menu=menu_1)
