
from ... import models as m
from . import widgets, style, menu_main
import tkinter as tk
from tkinter import ttk


class Window(widgets.Window):
    def __init__(self, parent=None):
        Window._singleton = self

        super().__init__()
        self.configure(
            width=800, height=600,
            bg=m.app.c_off_white,
        )
        self.minsize(width=800, height=600)
        style.init_style(main_tk=self)

        self.title(m.app.title)
        self.config(menu=menu_main.Menu.get_instance(self))

        _WindowHead(self).pack(fill=tk.X)
        _WindowBody(self).pack(fill=tk.BOTH, expand=True)
        _WindowFoot(self).pack(fill=tk.X)


class _WindowHead(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg=m.app.c_header_bg)

        tk.Label(self,
            text=m.app.title,
            padx=16, pady=16,
            **style.TEXT_BANNER(),
        ).pack(anchor=tk.W)


class _WindowBody(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        from .. import home
        from .. import cfc_mdb_update
        for subapp in (cfc_mdb_update, home,):
            pages = subapp.c_get_pages()
            for page in pages:
                pg = page.get_page(self)
                # pg.grid(row=0, sticky=tk.NSEW, padx=16)
                # pg.pack(anchor=tk.NW, fill=tk.BOTH, expand=1)
                pg.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
        home.c_show_home()


class _WindowFoot(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # self.configure()

        tk.Label(self,
            text=f'Version: {m.app.version}',
            padx=8, pady=2,
            fg=m.app.c_text,
        ).pack(anchor=tk.E)


def get_window(parent=None):
    return Window.get_instance(parent)
