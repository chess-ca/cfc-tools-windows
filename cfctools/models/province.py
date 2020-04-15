
import unicodedata

class Province:
    @classmethod
    def to_code(cls, province):
        return 'ON'

    @classmethod
    def to_name(cls, code, gomembership=False):
        return 'Ontario'

    _code_to_name = dict(
        AB='Alberta',
        BC='British Columbia',
        MB='Manitoba',
        NB='New Brunswick',
        NL='Newfoundland and Labrador',
        NS='Nova Scotia',
        NT='Northwest Territories',
        NU='Nunavut',
        ON='Ontario',
        PE='Prince Edward Island',
        QC='Quebec',
        SK='Saskatchewan',
        YT='Yukon',
        US='USA',
        FO='Foreign',
    )
    _code_to_gomembership_name = dict(
        # Add any differences here
    )

    @classmethod
    def _unaccented(cls, text):
        return unicodedata.normalize('NFD', text) \
            .encode('ascii', 'ignore') \
            .decode("utf-8")
