
from . import callbacks, widgets, style
import tkinter as tk


class Menu(widgets.Menu):

    def __init__(self, parent):
        super().__init__(parent)
        self._menu_style = style.TK_MENU()
        self.config(**self._menu_style)
        self._add_File_submenu()
        self._add_Tools_submenu()
        self._add_Help_submenu()

    def _add_File_submenu(self):
        menu_1 = tk.Menu(self, tearoff=False, **self._menu_style)
        # menu_1.add_command(
        #     label="Select file…",
        #     # command=self.callbacks['file->select'],
        #     accelerator='Ctrl+O'
        # )
        # menu_1.add_separator()
        menu_1.add_command(
            label="Exit",
            command=callbacks.CB_APP_QUIT,
            # accelerator='Ctrl+W'
        )
        self.add_cascade(label='File', menu=menu_1)

    def _add_Tools_submenu(self):
        menu_1 = tk.Menu(self, tearoff=False, **self._menu_style)
        menu_1.add_command(
            label='Home',
            command=callbacks.CB_HOME,
        )
        menu_1.add_separator()
        menu_1.add_command(
            label='Update cfc.mdb ...',
            command=callbacks.CB_CFC_MDB_UPDATE,
        )
        menu_1.add_command(
            label='Affiliate check ...',
            command=callbacks.CB_AFFILIATE_CHECK,
        )
        self.add_cascade(label='Tools', menu=menu_1)

    def _add_Help_submenu(self):
        menu_1 = tk.Menu(self, tearoff=False, **self._menu_style)
        # menu_1.add_command(
        #     label='Update cfc.mdb',
        #     #command=self.callbacks['file->quit'],
        # )
        self.add_cascade(label='Help', menu=menu_1)
