
import tkinter as tk
from tkinter import ttk
import cfctools.ui_graphical.application as app
from ..main import app_widgets


class HomePage(app_widgets.Page):
    def init_widget(self, parent, **kwargs):
        self.config(padding=(16,16,16,16),)
        self.columnconfigure(0, minsize=120)
        for i in [0,1,2]:
            self.rowconfigure(i, pad=8)

        # -------- Instruction
        ttk.Label(self,
            text='Select a function:',
        ).grid(row=0, column=0, columnspan=2, sticky=tk.SW,)

        # -------- Option: cfc_mdb_update
        ttk.Button(self,
            text='Go ...',
            command=app.Routes.CFC_MDB_UPDATE_ARGS,
        ).grid(row=1, column=0, sticky=tk.E,)
        ttk.Label(self,     # style=app_style.TTK_LABEL,
            text='Update a cfc*.mdb database\nwith data from GoMembership',
        ).grid(row=1, column=1, sticky=tk.W, padx=24,)

        # -------- Option: cfc_mdb_extract
        ttk.Button(self,
            text='Go ...',
            command=app.Routes.CFC_MDB_EXTRACT_ARGS,
        ).grid(row=2, column=0, sticky=tk.E,)
        ttk.Label(self,
            text='Extract data from a cfc*.mdb database\nfor updating server.chess.ca',
        ).grid(row=2, column=1, sticky=tk.W, padx=24,)
