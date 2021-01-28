
from .window_main import MainWindow
from .page_home import HomePage
from .page_wip import UnderConstructionPage


def init_pages(parent):
    HomePage(parent)
    UnderConstructionPage(parent)


