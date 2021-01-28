
import pathlib as pl
import zipapp

dir_app = pl.Path(__file__).parents[1]
f_pyzw = dir_app / 'x-dev' / 'CFC-Tools.pyzw'


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
    main='cfctools.application:run',
    filter=myfilter,
    compressed=True,
)
