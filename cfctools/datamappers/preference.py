
# Use: winreg ; See: https://docs.python.org/3/library/winreg.html
# ISSUE: types (str, int, ...) saved to & retrieved from Win Registry?
import winreg as wr
import pathlib

_regkeys = (wr.HKEY_CURRENT_USER, 'Software', 'CFC-Tools',)

# >>>> Not needed!?!?  The filedialog already remembers the last directory


def ZZZget_attrs(obj, attrs_to_get):
    fp = pathlib.Path('c:/CFC Home/CFC Files/CFCprograms')
    while not fp.is_dir():
        fp = fp.parent
    for attr in attrs_to_get:
        if hasattr(obj, attr):
            print(f'>>>> {k_cfc}\nattr={attr}')
            val_type = wr.QueryValueEx(k_cfc, attr)
            setattr(obj, attr, str(val_type[0] or ''))

def get_attrs(obj, attrs_to_get):
    # NOTE: Windows Registry is more complicated: has 32-bit and 64-bit views.
    #   - See: https://stackoverflow.com/questions/30932831/winreg-openkey-throws-filenotfound-error-for-existing-registry-keys
    #   - See:
    with wr.CreateKey(wr.HKEY_CURRENT_USER, 'Software\\CFC-Tools') as k_cfc:
        for attr in attrs_to_get:
            if hasattr(obj, attr):
                try:
                    val_type = wr.QueryValueEx(k_cfc, attr)
                    setattr(obj, attr, str(val_type[0] or ''))
                except FileNotFoundError:
                    setattr(obj, attr, '')


def save_attrs(obj, attrs_to_save):
    with wr.CreateKeyEx(_regkeys[0], _regkeys[1], access=wr.KEY_WRITE) as k_sw:
        with wr.CreateKeyEx(k_sw, _regkeys[2], access=wr.KEY_WRITE) as k_cfc:
            for attr in attrs_to_save:
                if hasattr(obj, attr):
                    val = getattr(obj, attr, '')
                    wr.SetValueEx(k_cfc, attr, wr.REG_SZ, val)
