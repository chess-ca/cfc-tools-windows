
from ..app import widgets, style, callbacks
import tkinter as tk
from tkinter import ttk
import pathlib


class Page(widgets.Page):
    def init_config(self, parent, **kwargs):
        self.w_vars.initialdir = tk.StringVar()
        self.w_vars.members_xlsx = tk.StringVar()
        self.w_vars.fields_xlsx = tk.StringVar()
        self.w_vars.cfc_mdb = tk.StringVar()
        self.w_vars.cfc_mdb_pw = tk.StringVar()

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
            text='Update cfc.mdb:', anchor=tk.W,
        ).grid(row=0, column=0, columnspan=3, sticky=tk.SW,)

        # ---- ---- Input Files
        f1 = ttk.Labelframe(self)
        f1.configure(text='INPUT files')
        f1.grid_columnconfigure(0, weight=1)
        f1w1 = widgets.LabelFileEntry(
            parent=f1,
            label='"All Members" report from GoMembership (.xlsx):',
            w_var=self.w_vars.members_xlsx,
            initialdir=self.w_vars.initialdir,
            filetypes=[('xlxs files', '*.xlsx'),('all files', '*.*')],
        )
        f1w1.grid(row=0, column=0, sticky=tk.EW)
        f1w2 = widgets.LabelFileEntry(
            parent=f1,
            label='"Members and Fields (NGB)" report from GoMembership (.xlsx):',
            w_var=self.w_vars.fields_xlsx,
            initialdir=self.w_vars.initialdir,
            filetypes=[('xlxs files', '*.xlsx'),('all files', '*.*')],
        )
        f1w2.grid(row=1, column=0, sticky=tk.EW)
        f1.grid(row=1, column=1, sticky=tk.EW)

        # ---- ---- Updated File
        f2 = ttk.Labelframe(self)
        f2.configure(text='UPDATED file')

        f2.grid_columnconfigure(0, weight=1)
        f2w1 = widgets.LabelFileEntry(
            parent=f2,
            label='"cfc*.mdb" CFC members/ratings database (.mdb):',
            w_var=self.w_vars.cfc_mdb,
            initialdir=self.w_vars.initialdir,
            filetypes=[('mdb files', '*.mdb'),('all files', '*.*')],
        )
        f2w1.grid(row=0, column=0, sticky=tk.EW)
        f2w2 = widgets.LabelEntry(
            parent=f2,
            label='Password (if required)',
            w_var=self.w_vars.cfc_mdb_pw,
        )
        f2w2.grid(row=1, column=0, sticky=tk.W)
        f2.grid(row=2, column=1, sticky=tk.EW)

        # ---- ---- (vertical space)
        self.grid_rowconfigure(3, minsize=48)

        # ---- ---- Buttons
        f4 = ttk.Frame(self)
        ttk.Button(f4,
            text='Update .mdb',
            command=self.update,
        ).pack(side=tk.LEFT, padx=8,)
        ttk.Button(f4,
            text='Cancel',
            command=callbacks.CB_HOME,
        ).pack(side=tk.LEFT, padx=8,)
        f4.grid(row=4, column=0, columnspan=3, sticky=tk.SW,)

    def update(self):
        callbacks.CB_CFC_MDB_UPDATE_RUN(
            members_xlsx=self.w_vars.members_xlsx.get(),
            fields_xlsx=self.w_vars.fields_xlsx.get(),
            cfc_mdb=self.w_vars.cfc_mdb.get(),
            cfc_mdb_pw=self.w_vars.cfc_mdb_pw.get(),
        )


def get_page(parent=None):
    return Page.get_instance(parent)
