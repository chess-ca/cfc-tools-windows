
from dataclasses import dataclass, field
from typing import ClassVar
import re

_re_dividers = re.compile(r'[,\s]+')
_result_codes = str.maketrans('WDL', '+=-')
_re_single_result = re.compile(r'([WDL+=-])\s*(\d+)')

@dataclass
class EventResult:
    event_id: int = 0
    place: int = 0

    cfc_id: int = 0
    province: str = ''
    games_played: int = 0
    score: float = 0
    results: str = ''

    rating_type: str = ''
    rating_pre: int = 0
    rating_perf: int = 0
    rating_post: int = 0
    rating_indicator: int = 0

    REGULAR: ClassVar[str] = 'R'
    QUICK: ClassVar[str] = 'Q'

    def set_results(self, results_str):
        pass

    @staticmethod
    def normalize_results(results, event_id=None):
        results = str(results or '').strip().upper()
        if 'X' in results:
            # It's a Round-Robin:
            # ("0=X111" or "0 = X 1 = 1") ==> "0|=|X|1|=|1"
            results = results.replace(' ', '')
            results = '|'.join([c for c in results])
        else:
            # It's a Swiss-Sys:
            # Older format: "W 11  L  7  D 10  W  9  W  12"
            # Newer format: "+18 -2 =10 +21 =11"
            original = results
            remainder = original
            results = results.translate(_result_codes)
            rset = []
            for m in _re_single_result.finditer(results):
                remainder = remainder[:m.start()]  \
                    + (' '*(m.end()-m.start()))  \
                    + remainder[m.end():]
                rset.append(m.group(1) + m.group(2))
            if remainder.strip() != '':
                print(f'Unexpected results for event {event_id}: {original}')
            results = '|'.join(rset)

        # Wrap in [...] to avoid having "=" as 1st char (spreadsheets will think it's a formula)
        results = f'[{results}]'
        return results
