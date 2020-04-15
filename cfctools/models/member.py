
from dataclasses import dataclass


@dataclass
class Member:
    cfc_id: str = None
    user_id: str = None
    address: str = ''
    city: str = ''
    province: str = ''
    gender: str = ''
