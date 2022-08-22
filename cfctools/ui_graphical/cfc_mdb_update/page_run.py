
import tkinter as tk, threading
from tkinter import ttk
import cfctools.ui_graphical.application as app
from ..main import app_widgets
from ...services import cfc_mdb_update


class RunPage(app_widgets.Page):
    def init_widget(self, parent, **kwargs):
        # ==== ==== ==== ==== Page Widgets
        self.config(padding=(16,16,16,16),)
        for i in [0,1,2,3]:
            self.grid_rowconfigure(i, pad=8)
        self.grid_columnconfigure(0, minsize=24)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self,
            text='Updating cfc.mdb:', anchor=tk.W,
        ).grid(row=0, column=0, columnspan=3, sticky=tk.SW,)

        # ---- ---- Update Log
        self.logbox = app_widgets.LoggerBox(self, height=20, width=100,)
        self.logbox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

        # ---- ---- (vertical space)
        self.grid_rowconfigure(3, minsize=48)

        # ---- ---- Buttons
        f4 = ttk.Frame(self)
        ttk.Button(f4,
            text='Home',
            command=app.Routes.HOME,
        ).pack(side=tk.LEFT, padx=8,)
        f4.grid(row=4, column=0, columnspan=3, sticky=tk.SW,)

    def before_showing(self, **kwargs):
        self.logbox.delete('1.0', tk.END)
        cfcmdb = kwargs.get('cfcmdb')
        self.logbox.activate(log_file=cfcmdb+'.update-log.txt')

    def after_showing(self, **kwargs):
        # app.update_gui()
        _Worker(**kwargs).start()


class _Worker(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__()
        self.members_xlsx = kwargs.get('members_xlsx')
        self.cfcmdb = kwargs.get('cfcmdb')
        self.cfcmdb_pw = kwargs.get('cfcmdb_pw')

    def run(self):
        cfc_mdb_update.update(self.members_xlsx, self.cfcmdb, self.cfcmdb_pw)
