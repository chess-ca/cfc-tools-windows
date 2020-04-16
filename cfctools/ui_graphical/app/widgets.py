
from . import style
import tkinter as tk
from tkinter import ttk


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


class LabelInput(ttk.Frame):
    def __init__(self, parent,
            w_class=None,           # tk/ttk widget class
            w_label=None,           # text for the label widget
            w_var=None,             # variable bound to this input
            w_label_config=None,    # config for the label widget
            w_input_config=None,    # config for the input widget
            **kwargs,               # for the Frame
    ):
        self.w_parent = parent
        super().__init__(parent, **kwargs)
