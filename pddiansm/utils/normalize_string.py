import unidecode


def _remove_accents(string: str) -> str:
    unaccented_string: str = unidecode.unidecode(string)
    return unaccented_string


def normalize_string(string: str) -> str:
    return _remove_accents(string).lower()
