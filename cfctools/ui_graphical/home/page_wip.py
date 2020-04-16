
from ... import models as m
from ..app import widgets, style, callbacks
import tkinter as tk
from tkinter import ttk


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):
        self.config(padding=(16,16,16,16),)
        self.grid_columnconfigure(0, minsize=120)
        for i in [0,1,2]:
            self.grid_rowconfigure(i, pad=8)

        ttk.Label(self, # **style.TEXT_REGULAR(), #padx=16, pady=16),
            text='UNDER CONSTRUCTION!',
        ).grid(row=0, column=0, columnspan=2, sticky=tk.SW,)

        ttk.Button(self,
            text='Home',
            command=callbacks.CB_HOME,
        ).grid(row=1, column=0, sticky=tk.SW,)
        self.grid_rowconfigure(1, minsize=128)


def get_page(parent=None):
    return Page.get_instance(parent)
