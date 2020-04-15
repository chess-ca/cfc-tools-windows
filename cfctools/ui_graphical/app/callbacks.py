
from ... import models as m
from .. import home
from .. import cfc_mdb_update as cmu


CB_HOME = home.c_show_home
CB_CFC_MDB_UPDATE = cmu.c_get_args
CB_CFC_MDB_UPDATE_RUN = cmu.c_do_update
CB_AFFILIATE_CHECK = home.c_show_wip


def R_APP_QUIT():   # since m.app.window_main is None at import-time
    m.app.window_main.quit()
