
from ... import models as m
from ..app import widgets, style, callbacks
import tkinter as tk
from tkinter import ttk


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):
        self.config(
            bg=m.app.c_off_white,
            padx=16,
        )
        self.columnconfigure(0, minsize=120)
        for i in [0,1,2]:
            self.rowconfigure(i, pad=8)

        tk.Label(self, **style.TEXT_REGULAR(), #padx=16, pady=16),
            text='UNDER CONSTRUCTION!',
        ).grid(row=0, column=0, columnspan=2, sticky=tk.SW,)

        ttk.Button(self,
            text='< HOME',
            command=callbacks.CB_HOME,
        ).grid(row=1, column=0, sticky=tk.SW,)
        self.grid_rowconfigure(1, minsize=128)


def get_page(parent=None):
    return Page.get_instance(parent)
