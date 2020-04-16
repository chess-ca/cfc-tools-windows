
from ... import models as m
from ..app import widgets, style, callbacks
import tkinter as tk
from tkinter import ttk


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):
        self.config(padding=(16,16,16,16),)
        for i in [0,1,2,3]:
            self.grid_rowconfigure(i, pad=8)
        self.grid_columnconfigure(0, minsize=24)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self,
            text='Update cfc.mdb:', anchor=tk.W,
        ).grid(row=0, column=0, columnspan=3, sticky=tk.SW,)

        # ---- ---- Input Files
        f = _FrameInputFiles(self)
        f.grid(row=1, column=1, sticky=tk.EW)
        # ---- ---- Updated File
        f = _FrameUpdatedFile(self)
        f.grid(row=2, column=1, sticky=tk.EW)
        # ---- ---- (space)
        self.grid_rowconfigure(3, minsize=48)
        # ---- ---- Buttons
        f = ttk.Frame(self)
        ttk.Button(f,
            text='Update .mdb',
            command=callbacks.CB_HOME,
        ).pack(side=tk.LEFT, padx=8,)
        ttk.Button(f,
            text='Cancel',
            command=callbacks.CB_HOME,
        ).pack(side=tk.LEFT, padx=8,)
        f.grid(row=4, column=0, columnspan=3, sticky=tk.SW,)



class _FrameInputFiles(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='INPUT files')

        ttk.Button(self,
            text='Yada Yada'
        ).grid(row=0, column=0, sticky=tk.W)


class _FrameUpdatedFile(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='UPDATED file')

        ttk.Button(self,
            text='Yada Yada'
        ).grid(row=0, column=0, sticky=tk.W)


def get_page(parent=None):
    return Page.get_instance(parent)
