
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

_font_family = 'Calibri'
_font = (_font_family, 14)
_bg = dict(background=c_bg)
_fgbg = dict(foreground=c_text, background=c_bg)

_styles = {
    'TFrame': dict(**_bg),
    'WindowHead.TFrame': dict(background=c_p400,),
    'TLabel': dict(font=_font, padx=8, **_fgbg),
    'WindowHead.TLabel': dict(font=(_font_family, 24, 'bold'), background=c_p400),
    'TLabelframe': dict(padding=(12,12,), **_bg),
    'TLabelframe.Label': dict(**_fgbg),
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
