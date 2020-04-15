
from . import page_get_args


def c_get_args(*args, **kwargs):
    page = page_get_args.get_page()
    page.show()


def c_do_update(*args, **kwargs):
    pass


def c_get_pages():
    return (page_get_args, )
