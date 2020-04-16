
from cfctools import ui_cmdline
from cfctools import ui_graphical


def main():
    args = ui_cmdline.args_parse()
    if args.action:     # if action was specified in the args ...
        # ... run as a command line app
        app = ui_cmdline.Application()
        app.run(args=args)
    else:
        # ... run as a GUI app
        app = ui_graphical.Application()
        app.run(args=args)


if __name__ == '__main__':
    main()
