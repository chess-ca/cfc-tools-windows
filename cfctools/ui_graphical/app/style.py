
from tkinter import ttk
from tkinter import font as tk_font
from functools import partial

# ---- ---- ---- ---- Colours
# Brand - Primary
# c_p900 = '#475b34'    # hsl(90,27%,28%)
# c_p800 = '#597141'    # hsl(90,27%,35%)
c_p600 = '#759556'    # hsl(90,27%,46%)
c_p500 = '#8cab6d'    # hsl(90,27%,55%)
c_p400 = '#a6be8e'    # hsl(90,27%,65%)
# c_p300 = '#ccdabe'    # hsl(90,27%,80%)
# c_p200 = '#e6ecdf'    # hsl(90,27%,90%)
c_p100 = '#f2f6ef'    # hsl(90,27%,95%)
c_text = '#404040'
c_bg = '#fefbf6'

# ==== ==== ==== ==== TTK: Style for ttk Widgets
PAGE = 'TFrame'
LABEL = 'TLabel'
LABEL_INPUT = 'Input.TLabel'
ENTRY_INPUT = 'Input.TEntry'
FILE_BUTTON = 'File.TButton'

_font_family = 'Calibri'
_font = f'{_font_family} 14'
_bg = dict(background=c_bg)
_fgbg = dict(foreground=c_text, background=c_bg)

_styles = {
    PAGE: dict(**_bg),
    'WindowHead.TFrame': dict(background=c_p400,),
    'Input.TFrame': dict(background='red',),
    'TLabel': dict(font=_font, padx=8, **_fgbg),
    'WindowHead.TLabel': dict(font=f'{_font_family} 24 bold', background=c_p400),
    'Input.TLabel': dict(font=f'{_font_family} 12'),
    'TLabelframe': dict(padding=(12,12,), **_bg),
    'TLabelframe.Label': dict(**_fgbg),
    'Input.TEntry': dict(),
    'File.TButton': dict(padding=(-2,-2,)),
    'TButton': dict(font=(_font_family, 12),),
}

def init_style(main_tk):
    s = ttk.Style()
    for sname, sargs in _styles.items():
        s.configure(sname, **sargs)


# ==== ==== ==== ==== TK: Style for tk Widgets
def _style(defaults, **overrides):
    style = defaults.copy()
    style.update(overrides)
    if 'font' in style and type(style['font']) == dict:
        style['font'] = tk_font.Font(**style['font'])
    return style

TK_MENU = partial(_style, dict(
    fg=c_text, bg=c_bg,
    font=dict(size=18, family='Calibri'),
))

# ======================================================================
# Notes:
#   - Ttk styles cannot be set before the Tk() object is created.
#     Therefore, must be set in a call to "init_style" function
#     instead of when this module is imported.
