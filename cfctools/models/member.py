# ======================================================================
# Here's some pydoc for CFC Member / Chess Player:
# ======================================================================
from dataclasses import dataclass


@dataclass
class Member:
    # ---- Member:
    #  - Represents a current or past member of the CFC.
    #  x""CFC Member / Chess Player:"""
    cfc_id: int = 0
    cfc_expiry: str = ''
    cfc_type: str = ''              # (see notes below)
    gomembership_id: str = ''
    fide_id: int = 0

    name_first: str = ''
    name_last: str = ''
    birthdate: str = ''
    gender: str = ''

    email: str = ''
    phone: str = ''
    # DEPRECATING address: str = ''
    addr_line1: str = ''
    addr_line2: str = ''
    addr_city: str = ''
    addr_province: str = ''
    addr_postalcode: str = ''

    regular_rating: int = 0
    regular_indicator: int = 0      # provisional games if < 50 else highest
    quick_rating: int = 0
    quick_indicator: int = 0        # provisional games if < 50 else highest

    notes: str = ''
    last_update: str = ''

    def __post_init__(self):
        pass
