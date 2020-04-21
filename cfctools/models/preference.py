
from .. import datamappers as dm

# >>>> Not needed!?!?  The filedialog already remembers the last directory

class PreferencesForWindows:
    def __init__(self, subkeys=None):
        # ---- Perference values (with defaults; before loading)
        self.dir_gomembership_data = 'c:\\'
        self.dir_cfc_mdb = 'c:\\'
        self._load_from_windows_registry()

    def save(self, list=None):
        attrs = list or self._preference_keys()
        dm.preference.save_attrs(self, attrs_to_save=attrs)

    def _load_from_windows_registry(self):
        attrs = self._preference_keys()
        dm.preference.get_attrs(self, attrs_to_get=attrs)

    def _preference_keys(self):
        return [k for k in self.__dict__.keys() if not k.startswith('_')]


preference = PreferencesForWindows()
