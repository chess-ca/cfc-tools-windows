
from .. import models as m
from .app import window_main


class Application():
    def __init__(self):
        m.app.instance = self
        m.app.window_main = window_main.get_window()

    def quit(self):
        m.app.window_main.quit()

    def run(self, args=None):
        m.app.window_main.mainloop()
