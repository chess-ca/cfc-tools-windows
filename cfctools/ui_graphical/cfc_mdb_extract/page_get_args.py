
import pathlib, datetime, tkinter as tk
from tkinter import ttk
import cfctools.ui_graphical.application as app
from ..main import app_widgets


class GetArgsPage(app_widgets.Page):
    def init_widget(self, parent, **kwargs):
        self.w_vars.initialdir = tk.StringVar()
        self.w_vars.cfc_mdb = tk.StringVar()
        self.w_vars.cfc_mdb_pw = tk.StringVar()
        self.w_vars.updated_text = tk.StringVar()
        self.w_vars.updated_text.set(datetime.datetime.now().strftime('%Y-%m-%d'))

        fp = pathlib.Path('c:/CFC Home/CFC Files/CFCPrograms')
        while not fp.is_dir():
            fp = fp.parent
        self.w_vars.initialdir.set(str(fp))

        # ==== ==== ==== ==== Page Widgets
        self.config(padding=(16,16,16,16),)
        for i in [0,1,2,3]:
            self.grid_rowconfigure(i, pad=8)
        self.grid_columnconfigure(0, minsize=24)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self,
            text='Extract from cfc*.mdb:', anchor=tk.W,
        ).grid(row=0, column=0, columnspan=3, sticky=tk.SW,)

        # ---- ---- Input File
        f1 = ttk.Labelframe(self)
        f1.configure(text='INPUT')
        f1.grid_columnconfigure(0, weight=1)
        f1w1 = app_widgets.LabelFileEntry(
            parent=f1,
            label='"cfc*.mdb" CFC members/ratings database:',
            w_var=self.w_vars.cfc_mdb,
            initialdir=self.w_vars.initialdir,
            filetypes=[('mdb files', '*.mdb'),('all files', '*.*')],
        )
        f1w1.grid(row=0, column=0, sticky=tk.EW)
        f1w2 = app_widgets.LabelEntry(
            parent=f1,
            label='Password (if required)',
            w_var=self.w_vars.cfc_mdb_pw,
        )
        f1w2.grid(row=1, column=0, sticky=tk.W)
        f1.grid(row=1, column=1, sticky=tk.EW)

        # ---- ---- Input File
        f2 = ttk.Labelframe(self)
        f2.configure(text='OUTPUT')
        f2.grid_columnconfigure(0, weight=1)
        f2w1 = app_widgets.LabelEntry(
            parent=f2,
            label='"Updated" text (visible on the website)',
            w_var=self.w_vars.updated_text,
        )
        f2w1.grid(row=2, column=0, sticky=tk.W)
        f2.grid(row=2, column=1, sticky=tk.EW)

        # ---- ---- (vertical space)
        self.grid_rowconfigure(3, minsize=48)

        # ---- ---- Buttons
        f4 = ttk.Frame(self)
        ttk.Button(f4,
            text='Extract',
            command=self.do_extract,
        ).pack(side=tk.LEFT, padx=8,)
        ttk.Button(f4,
            text='Cancel',
            command=app.Routes.HOME,
        ).pack(side=tk.LEFT, padx=8,)
        f4.grid(row=4, column=0, columnspan=3, sticky=tk.SW,)

    def do_extract(self):
        app.Routes.CFC_MDB_EXTRACT_RUN(
            cfcmdb=self.w_vars.cfc_mdb.get(),
            cfcmdb_pw=self.w_vars.cfc_mdb_pw.get(),
            updated_text=self.w_vars.updated_text.get(),
        )
