# ======================================================================
# application.run():
# - Run the app as either command line (cli) or graphical (gui)
#   depending if an action was specified in the invocation args.
# ======================================================================
from cfctools.ui_cmdline.parse_args import parse_args


def run():
    args = parse_args()
    if hasattr(args, 'action') and args.action:
        _run_cmdline(args)
    else:
        _run_graphical(args)


def _run_cmdline(args):
    from cfctools.ui_cmdline.application import Application as CLI_Application
    app = CLI_Application()
    app.run(args=args)


def _run_graphical(args):
    from cfctools.ui_graphical.application import Application as GUI_Application
    app = GUI_Application()
    app.run(args=args)
    # from cfctools.ui_graphical import application as zzz

