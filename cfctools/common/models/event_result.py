
from dataclasses import dataclass, field
from typing import ClassVar
import re

_re_dividers = re.compile(r'[,\s]+')
_result_codes = str.maketrans('WDL', '+=-')

@dataclass
class EventResult:
    event_id: int = 0
    place: int = 0

    cfc_id: int = 0
    province: str = ''
    games_played: int = 0
    score: int = 0
    results: str = ''

    rating_type: str = ''
    rating_pre: int = 0
    rating_perf: int = 0
    rating_post: int = 0

    REGULAR: ClassVar[str] = 'R'
    QUICK: ClassVar[str] = 'Q'

    def set_results(self, results_str):
        pass

    @staticmethod
    def normalize_results(results):
        # For Swiss Sys:  +18|-2|=10|+21|=11
        results = str(results or '').strip().upper()
        if 'X' in results:
            # It's a Round-Robin: "0=X111" ==> "0|=|X|1|1|1"
            results = '|'.join([c for c in results])
        else:
            # It's a Swiss-Sys: ==> "+18|-2|=10|+21|=11"
            results = _re_dividers.sub('|', results).translate(_result_codes)
        return results
