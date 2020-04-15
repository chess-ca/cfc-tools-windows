
import pyodbc
import sys, platform

pa = platform.architecture()
vi = sys.version_info
version = '\n'.join((
    f'Python {vi.major}.{vi.minor}.{vi.micro} {pa[0]}',
    f'pyodbc {pyodbc.version}',
    f'{pa[1]} {sys.getwindowsversion().major}',
))

print(f'version:\n{version}')
