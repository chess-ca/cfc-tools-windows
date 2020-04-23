
from .. import services

class Application:
    def run(self, args=None):
        # print('views_cmd.Application: invoked with args:', args)

        args = dict(
            members_xlsx=args.cmu_members,
            fields_xlsx=args.cmu_fields,
            cfc_mdb=args.cmu_cfcmdb,
            cfc_mdb_pw=args.cmu_cfcmdb_pw,
        )
        for t in services.cfc_mdb_update.update(**args):
            print(t[0:-1] if t[-1:] == '\n' else t)
