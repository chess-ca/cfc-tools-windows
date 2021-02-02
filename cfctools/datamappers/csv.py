# ======================================================================
# Class: CsvInMemory:
# - For creating a .csv (comma separated value) file in memory
#   so that it may written to a zipfile (Python core library)
# - Rows written to the .csv are often dataclasses (Python core)
#   so, as a convenience, convert these to dicts before writing to csv.
# ======================================================================
import io, csv, dataclasses

class CsvInMemory:
    def __init__(self, class_fields):
        self._csv_iostr = None
        self._csv_writer = None
        self._n_rows_in_current_csv = 0
        if isinstance(class_fields, list):
            self.fields = class_fields
        else:
            self.fields = [f.name for f in dataclasses.fields(class_fields)]

    def __len__(self):
        return self._n_rows_in_current_csv

    def writerow(self, row):
        if not isinstance(row, dict):
            row = dataclasses.asdict(row)
        self._get_csv_writer().writerow(row)
        self._n_rows_in_current_csv += 1

    def get_string(self):
        return self._csv_iostr.getvalue()

    def flush_to_zipfile(self, filename, zipfile):
        if self._n_rows_in_current_csv == 0:
            return
        zipfile.writestr(filename, self._csv_iostr.getvalue())
        self._csv_iostr = self._csv_writer = None
        self._n_rows_in_current_csv = 0

    def _get_csv_writer(self):
        if self._csv_writer is None:
            self._csv_iostr = io.StringIO(newline='')
            self._csv_writer = csv.DictWriter(self._csv_iostr, fieldnames=self.fields)
            self._csv_writer.writeheader()
            self._n_rows_in_current_csv = 0
        return self._csv_writer
