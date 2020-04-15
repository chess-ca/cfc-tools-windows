
from ... import models as m
import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font
from functools import partial


def _style(defaults, **overrides):
    style = defaults.copy()
    style.update(overrides)
    if 'font' in style and type(style['font']) == dict:
        style['font'] = tk_font.Font(**style['font'])
    return style

TEXT_BANNER = partial(_style, dict(
    fg=m.app.c_text, bg=m.app.c_header_bg,
    font=dict(size=24, family='Calibri', weight=tk_font.BOLD),
))
TEXT_REGULAR = partial(_style, dict(
    fg=m.app.c_text, bg=m.app.c_off_white,
    font=dict(size=14, family='Calibri'),
))
TEXT_H1 = partial(_style, dict(
    fg=m.app.c_text, bg=m.app.c_off_white,
    font=dict(size=18, weight=tk_font.BOLD),
))

DEFAULT_SECTION = dict(
    bg=m.app.c_off_white,
)


def init_style(main_tk):
    s = ttk.Style()
    s.configure('TButton',
        font=('Calibri', 12),
    )
