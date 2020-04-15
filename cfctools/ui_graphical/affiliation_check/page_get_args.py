
from ... import models as m
from ..app import widgets, style, callbacks
import tkinter as tk
# from tkinter import ttk


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):
        self.config(bg=m.app.c_off_white)

        tk.Label(self, **style.TEXT_REGULAR(padx=16, pady=16),
            text='Affiliation Check',
        ).grid(row=1, column=0, sticky=tk.W,)

        # ttk.Button(self, **v.style.BUTTON(),
        #     text='Go ...',
        #     command=callbacks.CB_CFC_MDB_UPDATE,
        # ).grid(row=2, column=0, sticky=tk.NE,)

        tk.Label(self, **v.style.TEXT_REGULAR(padx=16, justify='left'),
            text='Find members where the province of their address'
                '\ndoes not match the province of their membership affiliation.',
        ).grid(row=2, column=2, sticky=tk.NW,)


def get_page(parent=None):
    return Page.get_instance(parent)
