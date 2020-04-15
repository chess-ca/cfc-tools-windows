
from . import page_home
from . import page_wip


def c_show_home(*args, **kwargs):
    page = page_home.get_page()
    page.show()


def c_show_wip(*args, **kwargs):
    page = page_wip.get_page()
    page.show()


def c_get_pages():
    return (page_home, page_wip)
