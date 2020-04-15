
from ... import models as m
from ..app import widgets, style, callbacks
import tkinter as tk
from tkinter import ttk


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):
        self.config(bg=m.app.c_off_white, padx=16,)
        self.columnconfigure(0, minsize=120)
        for i in [0,1,2]:
            self.rowconfigure(i, pad=8)

        tk.Label(self, **style.TEXT_REGULAR(),
            text='Update cfc.mdb:',
        ).grid(row=0, column=0, sticky=tk.SW,)

        # ttk.LabelFrame(self)

        # ttk.Button(self,
        #     text='Go ...',
        #     command=callbacks.CB_CFC_MDB_UPDATE,
        # ).grid(row=2, column=0, sticky=tk.NE,)
        #
        # tk.Label(self, **v.style.TEXT_REGULAR(padx=16, justify='left'),
        #     text='Update a cfc.mdb database with data from GoMembership',
        # ).grid(row=2, column=2, sticky=tk.NW,)


def get_page(parent=None):
    return Page.get_instance(parent)
