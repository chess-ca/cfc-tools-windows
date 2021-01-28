
from .page_get_args import GetArgsPage
from .page_run import RunPage


def init_pages(parent):
    GetArgsPage.create_singleton(parent=parent)
    RunPage.create_singleton(parent=parent)
