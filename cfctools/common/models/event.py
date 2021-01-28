
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Event:
    id: int = 0
    name: str = ''
    date_end: str = ''
    province: str = ''
    arbiter_id: int = 0
    organizer_id: int = 0

    pairings: str = ''          # RR | SS
    rating_type: str = ''       # R=Regular | Q=Quick
    n_players: int = 0          # number of players
    n_rounds: int = 0           # number of rounds

    REGULAR: ClassVar[str] = 'R'
    QUICK: ClassVar[str] = 'Q'
    ROUND_ROBIN: ClassVar[str] = 'RR'
    SWISS_SYS: ClassVar[str] = 'SS'
