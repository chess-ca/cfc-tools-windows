
from ... import models as m
from ..app import widgets, style, callbacks
import tkinter as tk
from tkinter import ttk


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):
        self.config(padding=(16,16,16,16),)
        self.columnconfigure(0, minsize=120)
        for i in [0,1,2]:
            self.rowconfigure(i, pad=8)

        # -------- Instruction
        ttk.Label(self,
            text='Select a function:',
        ).grid(row=0, column=0, columnspan=2, sticky=tk.SW,)

        # -------- Option
        ttk.Button(self,
            text='Go ...',
            command=callbacks.CB_CFC_MDB_UPDATE,
        ).grid(row=1, column=0, sticky=tk.E,)

        # ttk.Label(self, style=style.TTK_LABEL,
        #     text='Update a cfc.mdb database\nwith data from GoMembership',
        # ).grid(row=1, column=1, sticky=tk.W, padx=24,)
        ttk.Label(self,
            text='Update a cfc.mdb database\nwith data from GoMembership',
        ).grid(row=1, column=1, sticky=tk.W, padx=24,)

        # -------- Option
        ttk.Button(self,
            text='Go ...',
            command=callbacks.CB_AFFILIATE_CHECK,
        ).grid(row=2, column=0, sticky=tk.E,)

        ttk.Label(self,
            text='Affiliation check:  members whose provincial affilation'
                 '\ndoes not match the province of their address.',
        ).grid(row=2, column=1, sticky=tk.W, padx=24,)


def get_page(parent=None):
    return Page.get_instance(parent)
