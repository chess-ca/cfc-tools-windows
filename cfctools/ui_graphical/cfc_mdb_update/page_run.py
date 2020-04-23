
from ..app import widgets, style, callbacks
import tkinter as tk
from tkinter import ttk, scrolledtext
import pathlib


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):

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
        self.logbox = scrolledtext.ScrolledText(self,
            height=20, width=100,
        )
        self.logbox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

        # ---- ---- (vertical space)
        self.grid_rowconfigure(3, minsize=48)

        # ---- ---- Buttons
        f4 = ttk.Frame(self)
        ttk.Button(f4,
            text='Home',
            command=callbacks.CB_HOME,
        ).pack(side=tk.LEFT, padx=8,)
        f4.grid(row=4, column=0, columnspan=3, sticky=tk.SW,)

    def reset(self):
        self.logbox.delete('1.0', tk.END)

    def append(self, text):
        self.logbox.insert(tk.END, text)
        self.logbox.yview(tk.END)


def get_page(parent=None):
    return Page.get_instance(parent)
