
import pathlib, sys, unittest
root = pathlib.Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from ..datamappers.job import JobFile


class TestJobFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.jobfile_path = pathlib.Path(__file__).resolve().parent / 'zzz.unittest.jobfile.zip'

    @classmethod
    def tearDownClass(cls):
        if cls.jobfile_path.exists():
            # self.jobfile_path.unlink()
            pass

    def test_1(self):
        jf = JobFile(
            str(self.jobfile_path), mode='w',
            title='Data from cfc*.mdb (MS-Access)',
            handler='update-from-mdb'
        )
        jf.comment('Created using CFC-Tools')
        jf.comment('I think it was Bob that created this')
        jf.comment('Not sure; maybe?')
        jf.args['api_version'] = 1.0
        jf.args['zootka'] = 'filburmore'
        jf.args['start-date'] = '2021-01-20-120000'
        data = ['first', 'second', 'third']
        jf.writestr('data.0001.txt', '\n'.join(data))
        data = ['zippity', 'dooooooo', 'daaaaaaaaa']
        jf.writestr('data.0002.txt', '\n'.join(data))
        jf.close()


if __name__ == '__main__':
    unittest.main()