
import zipfile as zf, datetime as dt, configparser, io


class JobFile:
    def __init__(self,
        filepath, mode='r',
        title=None, handler=None, args=None,
    ):
        self.filepath = filepath            # pathlib.Path | str
        self.zipfile = None
        self.mode = mode.lower()
        self.title = title or '(undefined)'
        self.handler = handler or 'undefined'
        self.args = args or dict()

        self._now = dt.datetime.utcnow()
        self.created = self._now
        self.next_try = self._now
        self.submit_by = ''
        self._comments = []

        self.set_submit_by(3*60)            # default: 3 hours to submit
        self.zipfile = zf.ZipFile(
            str(self.filepath),
            mode=self.mode,
            compression=zf.ZIP_DEFLATED
        )

    def writestr(self, fname, data):
        self.zipfile.writestr(fname, data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def comment(self, text):
        self._comments.append(text)

    def set_submit_by(self, when):
        if isinstance(when, int):
            delta = dt.timedelta(minutes=when)
            self.submit_by = self._now + delta
        elif isinstance(when, (dt.datetime, str,)):
            self.submit_by = when

    def write_job_ini(self):
        cp = configparser.ConfigParser()
        cp.add_section('JOB')
        job = cp['JOB']
        job['title'] = self.title
        job['handler'] = self.handler
        job['created'] = str(self.created)
        job['submit_by'] = str(self.submit_by)
        job['next_try'] = str(self.next_try)
        job['comments'] = '\n'.join(self._comments)
        cp.add_section('ARGS')
        args = cp['ARGS']
        for key, value in self.args.items():
            args[key] = str(value)
        config = io.StringIO()
        cp.write(config)
        self.writestr('job.ini', config.getvalue())

    def get_filename(self):
        return str(self.filepath)

    def close(self):
        if self.mode == 'w':
            self.write_job_ini()
        self.zipfile.close()
