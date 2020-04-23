
from . import page_get_args
from . import page_run
from ... import services
import threading


def c_get_args(*args, **kwargs):
    page = page_get_args.get_page()
    page.show()


def c_do_update(members_xlsx, fields_xlsx, cfc_mdb, cfc_mdb_pw):
    page = page_run.get_page()
    page.reset()
    page.show()
    args = dict(
        members_xlsx=members_xlsx,
        fields_xlsx=fields_xlsx,
        cfc_mdb=cfc_mdb,
        cfc_mdb_pw=cfc_mdb_pw,
    )
    Worker(page, args).start()


class Worker(threading.Thread):
    def __init__(self, page, args):
        super().__init__()
        self.page = page
        self.args = args

    def run(self):
        for t in services.cfc_mdb_update.update(**self.args):
            self.page.append(t)


def c_get_pages():
    return (page_get_args, page_run,)
