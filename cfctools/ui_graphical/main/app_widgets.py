
import logging, pathlib, types
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from . import app_style


# ======================================================================
# Mixins
# ======================================================================
class SingletonMixin:
    w_singleton = None

    @classmethod
    def create_singleton(cls, **kwargs):
        cls.w_singleton = cls(**kwargs)
        return cls.w_singleton

    @classmethod
    def get_singleton(cls):
        if cls.w_singleton is None:
            raise Exception('Singleton undefined; use .create_singleton() first')
        return cls.w_singleton


class TitleMixin:
    # Pass the title up (until an ancestor handles it)
    def w_set_title(self, parent, title=None):
        if hasattr(parent, 'w_set_title'):
            parent.set_title(title)


# ======================================================================
# Widgets
# ======================================================================
class Window(SingletonMixin, tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_widget(**kwargs)

    def init_widget(self, **kwargs):
        pass

    @classmethod
    def exit_window(cls):
        cls.get_singleton().quit()


class Menu(SingletonMixin, tk.Menu):
    pass


class Page(SingletonMixin, ttk.Frame):
    w_singleton = None

    def __init__(self, parent, **kwargs):
        self.__class__.w_singleton = self
        self.w_parent = parent
        self.w_vars = types.SimpleNamespace()
        kwargs['style'] = kwargs.get('style', app_style.PAGE)
        super().__init__(parent, **kwargs)
        self.init_widget(parent, **kwargs)
        self.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    def init_widget(self, parent, **kwargs):
        pass

    def before_showing(self, **kwargs):
        pass

    def after_showing(self, **kwargs):
        pass

    @classmethod
    def show(cls, **kwargs):
        # (.show is a classmethod so it can be a Route without needing an instance)
        if cls.w_singleton is None:
            raise Exception('Page was not instantiated (w_singleton is None)')
        cls.w_singleton.before_showing(**kwargs)
        cls.w_singleton.lift()
        cls.w_singleton.after_showing(**kwargs)


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
        self.label = ttk.Label(self, text=label, style=app_style.LABEL_INPUT, **label_config)
        self.label.grid(row=0, column=0, sticky=tk.EW)
        self.input = ttk.Entry(self, style=app_style.ENTRY_INPUT, **input_config)
        self.input.grid(row=1, column=0, sticky=tk.EW)


# ---------------------------------------------------------------------
class LabelFileEntry(ttk.Frame):
    # - a widget for entering a file name/path
    # - includes a label, text for name/path, and file chooser dialog
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
        self.label = ttk.Label(self, text=self.label, style=app_style.LABEL_INPUT, **label_config)
        self.label.grid(row=0, column=0, sticky=tk.EW)
        self.input = ttk.Entry(self, style=app_style.ENTRY_INPUT, **input_config)
        self.input.grid(row=1, column=0, sticky=tk.EW)
        self.select = ttk.Button(self, text='select', width=6, style=app_style.FILE_BUTTON,
            command=self.filedialog)
        self.select.grid(row=1, column=1, sticky=tk.E)

    def filedialog(self):
        initdir = self.w_initialdir.get() or 'c:/'
        fp = filedialog.askopenfilename(title=self.label, initialdir=initdir, filetypes=self.w_filetypes)
        fp = pathlib.Path(fp)
        if fp.exists() and not fp.is_dir():
            self.w_var.set(str(fp).replace('/', '\\'))
            self.w_initialdir.set(str(fp.parent))


# ---------------------------------------------------------------------
class LoggerBox(scrolledtext.ScrolledText):
    # Displays whatever is written to the "console" log (done by a service)
    def activate(self, log_file=None):
        logger = logging.getLogger('console')
        for h in logger.handlers:
            logger.removeHandler(h)
        logger.addHandler(logging.StreamHandler(stream=self))
        if log_file:
            logger.addHandler(logging.FileHandler(str(log_file), mode='a'))
        logger.setLevel(logging.INFO)

    def write(self, text_nl):
        self.insert(tk.END, text_nl)
        self.yview(tk.END)

    def flush(self):    # required by logging.StreamHandler
        pass
