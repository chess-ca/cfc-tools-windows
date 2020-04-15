
# Use: winreg ; See: https://docs.python.org/3/library/winreg.html
# ISSUE: types (str, int, ...) saved to & retrieved from Win Registry?
import winreg as wr

_regkeys = (wr.HKEY_CURRENT_USER, 'Software', 'CFC-Tools',)


def get_attrs(obj, attrs_to_get):
    with wr.CreateKeyEx(_regkeys[0], _regkeys[1], access=wr.KEY_READ) as k_sw:
        with wr.CreateKeyEx(k_sw, _regkeys[2], access=wr.KEY_READ) as k_cfc:
            for key in attrs_to_get:
                pass
        # TODO: get values from Windows registry
        # 1) get values from Windows registry
        # 2) if hasattr(self, name), then set it (replace default).
        # 3) otherwise, delete it from Windows Registry.


def save_attrs(obj, attrs_to_save):
    with wr.CreateKeyEx(_regkeys[0], _regkeys[1], access=wr.KEY_WRITE) as k_sw:
        with wr.CreateKeyEx(k_sw, _regkeys[2], access=wr.KEY_WRITE) as k_cfc:
            for key in attrs_to_save:
                pass
                # TODO: save key/value to Windows Registry
