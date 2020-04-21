
from . import style
import tkinter as tk
from tkinter import ttk, filedialog
import pathlib, types


class SingletonMixin:
    _w_singleton = None

    @classmethod
    def get_instance(cls, parent=None):
        if cls._w_singleton is None:
            cls._w_singleton = cls(parent) if parent else cls()
        return cls._w_singleton


class TitleMixin:
    # Pass the title up (until an ancestor handles it)
    def w_set_title(self, parent, title=None):
        if hasattr(parent, 'w_set_title'):
            parent.set_title(title)


class Window(SingletonMixin, TitleMixin, tk.Tk):
    pass


class Menu(SingletonMixin, tk.Menu):
    pass


class Page(SingletonMixin, ttk.Frame):
    w_title = ''

    def __init__(self, parent, **kwargs):
        self.w_parent = parent
        self.w_vars = types.SimpleNamespace()
        kwargs['style'] = kwargs.get('style', style.PAGE)
        super().__init__(parent, **kwargs)
        self.init_config(parent)

    def init_config(self, parent, **kwargs):
        pass

    def set_title(self, title=None):
        if title is None:
            title = getattr(self, 'title', '')
        if hasattr(self.w_parent, 'set_title'):
            self.w_parent.set_title(title)

    def before_show(self):
        pass

    def show(self):
        self.set_title()
        self.before_show()
        self.lift()


class TtkPage(SingletonMixin, ttk.Frame):
    def __init__(self, parent=None, **kwargs):
        self._parent = parent
        super().__init__(parent)
        self.init_config(parent, **kwargs)

    def init_config(self, parent, **kwargs):
        pass

    def set_title(self, title=None):
        if title is None:
            title = getattr(self, 'title', '')
        if hasattr(self._parent, 'set_title'):
            self._parent.set_title(title)

    def before_show(self):
        pass

    def show(self):
        self.set_title()
        self.before_show()
        self.lift()


class LabelEntry(ttk.Frame):
    def __init__(self, parent,
            label,                  # text for the label widget
            w_var,                  # variable bound to this input
            label_config=None,      # config for the label widget
            input_config=None,      # config for the input widget
            **kwargs,               # for the Frame
    ):
        self.w_parent = parent
        super().__init__(parent, **kwargs)
        label = label or ''
        label_config = label_config or {}
        input_config = input_config or {}
        input_config['textvariable'] = w_var

        self.grid_columnconfigure(0, weight=1)
        self.label = ttk.Label(self, text=label, style=style.LABEL_INPUT, **label_config)
        self.label.grid(row=0, column=0, sticky=tk.EW)
        self.input = ttk.Entry(self, style=style.ENTRY_INPUT, **input_config)
        self.input.grid(row=1, column=0, sticky=tk.EW)


class LabelFileEntry(ttk.Frame):
    def __init__(self, parent,
            # widget=None,            # tk/ttk widget class
            label,                  # text for the label widget
            w_var,                  # variable bound to this input
            initialdir,             # initial directory for file
            filetypes=None,         #
            label_config=None,      # config for the label widget
            input_config=None,      # config for the input widget
            **kwargs,               # for the Frame
    ):
        super().__init__(parent, **kwargs)
        self.w_parent = parent
        self.w_var = w_var
        self.w_initialdir = initialdir
        self.w_filetypes = filetypes or []
        self.label = label or ''
        label_config = label_config or {}
        input_config = input_config or {}
        input_config['textvariable'] = self.w_var

        self.grid_columnconfigure(0, weight=1)
        self.label = ttk.Label(self, text=self.label, style=style.LABEL_INPUT, **label_config)
        self.label.grid(row=0, column=0, sticky=tk.EW)
        self.input = ttk.Entry(self, style=style.ENTRY_INPUT, **input_config)
        self.input.grid(row=1, column=0, sticky=tk.EW)
        self.select = ttk.Button(self, text='select', width=6, style=style.FILE_BUTTON,
            command=self.filedialog)
        self.select.grid(row=1, column=1, sticky=tk.E)

    def filedialog(self):
        initdir = self.w_initialdir.get() or 'c:/'
        fp = filedialog.askopenfilename(title=self.label, initialdir=initdir, filetypes=self.w_filetypes)
        fp = pathlib.Path(fp)
        if fp.exists() and not fp.is_dir():
            self.w_var.set(str(fp).replace('/', '\\'))
            self.w_initialdir.set(str(fp.parent))
