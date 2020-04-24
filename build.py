
import pathlib as pl
import zipapp

dir_app = pl.Path(__file__).parent
f_pyzw = dir_app / 'CFC-Tools.pyzw'


def myfilter(filepath):
    fp = str(filepath)
    include = 'zzz' not in fp \
        and 'venv' not in fp \
        and '.pyzw' not in fp \
        and '.iml' not in fp \
        and '.git' not in fp \
        and '.idea' not in fp
    # if include:
    #     print(f'fp: {fp}')
    return include


zipapp.create_archive(
    dir_app,
    target=f_pyzw,
    # main=None,
    filter=myfilter,
    compressed=True,
)
