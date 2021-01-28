
import tkinter as tk, threading
from tkinter import ttk
import cfctools.ui_graphical.application as app
from ..main import app_widgets
from ...services import extract_from_mdb


class RunPage(app_widgets.Page):
    def init_widget(self, parent, **kwargs):

        # ==== ==== ==== ==== Page Widgets
        self.config(padding=(16,16,16,16),)
        for i in [0,1,2,3]:
            self.grid_rowconfigure(i, pad=8)
        self.grid_columnconfigure(0, minsize=24)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self,
            text='Extracting from a cfc*.mdb:', anchor=tk.W,
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
        self.logbox.activate()

    def after_showing(self, **kwargs):
        # app.update_gui()
        _Worker(**kwargs).start()


class _Worker(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__()
        self.cfcmdb = kwargs.get('cfcmdb')
        self.cfcmdb_pw = kwargs.get('cfcmdb_pw')
        self.updated_text = kwargs.get('updated_text', '')

    def run(self):
        extract_from_mdb.extract(self.cfcmdb, self.cfcmdb_pw, self.updated_text)
