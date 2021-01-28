
import tkinter as tk
from tkinter import ttk
import cfctools.ui_graphical.application as app
from ..main import app_widgets


class UnderConstructionPage(app_widgets.Page):
    def init_widget(self, parent, **kwargs):
        self.config(padding=(16,16,16,16),)
        self.grid_columnconfigure(0, minsize=120)
        for i in [0,1,2]:
            self.grid_rowconfigure(i, pad=8)

        ttk.Label(self,     # **app_style.TEXT_REGULAR(), #padx=16, pady=16),
            text='UNDER CONSTRUCTION!',
        ).grid(row=0, column=0, columnspan=2, sticky=tk.SW,)

        ttk.Button(self,
            text='Home',
            command=app.Routes.HOME,
        ).grid(row=1, column=0, sticky=tk.SW,)
        self.grid_rowconfigure(1, minsize=128)
