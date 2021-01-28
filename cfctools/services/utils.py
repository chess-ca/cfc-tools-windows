
import pyodbc
import openpyxl


def _province_to_pp(province):
    # This method handles variations in long names
    p = (province or '').upper()
    return None if province is None \
        else '' if type(province) != str \
        else 'AB' if 'ALB' in p \
        else 'BC' if 'BRI' in p \
        else 'MB' if 'MAN' in p \
        else 'NB' if 'BRU' in p \
        else 'NL' if 'FOU' in p \
        else 'NT' if 'WES' in p \
        else 'NS' if 'SCO' in p \
        else 'NU' if 'NUN' in p \
        else 'ON' if 'ONT' in p \
        else 'PE' if 'PRI' in p \
        else 'QC' if 'QU' in p \
        else 'SK' if 'SAS' in p \
        else 'YT' if 'YUK' in p \
        else 'US' if 'US' in p \
        else 'FO' if 'FO' in p \
        else province


class XLSX:
    def __init__(self, filename, sheetname):
        self.filename = filename
        self.sheetname = sheetname

    def get_all(self):
        wb = openpyxl.load_workbook(
            filename=self.filename,
            data_only=True, read_only=True
        )
        ws = wb[self.sheetname]
        keys = []
        is_first_row = True
        for row in ws.rows:
            if is_first_row:
                keys = [c.value for c in row]
                is_first_row = False
            else:
                vals = [c.value for c in row]
                if len(vals) < len(keys):
                    vals += (len(keys) - len(vals)) * ['']
                data = dict(zip(keys, vals))
                yield data


class MDB:
    def __init__(self, filename, password, table, key):
        self.filename = filename
        self.password = password
        self.table = table
        self.key = key
        self.dbconn = None

    def get_all(self, sort=None):
        dbcsr = self._get_dbconn().cursor()
        sql = f'select * from "{self.table}"'
        if sort:
            sql += ' order by ' + sort
        dbcsr.execute(sql)
        for row in dbcsr.fetchall():
            yield row
        dbcsr.close()

    def get_id(self, id):
        id = float(id)
        dbcsr = self._get_dbconn().cursor()
        sql = f'select * from "{self.table}" where "{self.key}" = ?'
        dbcsr.execute(sql, id)
        row = dbcsr.fetchone()
        dbcsr.close()
        return row

    def insert(self, mdb_row):
        cols = '"' + '","'.join(mdb_row.keys()) + '"'
        vals = mdb_row.values()
        valqs = ','.join(['?'] * len(vals))
        sql = f'insert into "{self.table}" ({cols}) values ({valqs});'
        dbcsr = self._get_dbconn().cursor()
        dbcsr.execute(sql, *vals)
        self._get_dbconn().commit()
        dbcsr.close()


    def update(self, mdb_row, cols=None):
        id = float(mdb_row[self.key])
        if cols is None:
            cols = [k for k in mdb_row.keys() if k != self.key]
        vals = [mdb_row[v] for v in cols] + [id]
        sets = '"' + '"=?,"'.join(cols) + '"=?'
        sql = f'update "{self.table}" set {sets} where "{self.key}"=?'
        # print(f'>>>> SQL: {sql} ; vals={len(vals)}')
        dbcsr = self._get_dbconn().cursor()
        dbcsr.execute(sql, *vals)
        self._get_dbconn().commit()
        dbcsr.close()

    def _get_dbconn(self):
        if self.dbconn is None:
            pyodbc.pooling = False
            driver = '{Microsoft Access Driver (*.mdb)}'
            dbdsn = f'DRIVER={driver};DBQ={self.filename};'    # error if DBQ has quotes
            if self.password:
                dbdsn += f'PWD={self.password};'
            self.dbconn = pyodbc.connect(dbdsn)
        return self.dbconn



# ----------------------------------------------------------------------
# Notes:
#   - Ref: https://github.com/mkleehammer/pyodbc/wiki/Tips-and-Tricks-by-Database-Platform
