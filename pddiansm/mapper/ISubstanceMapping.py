from typing import List


class ISubstanceMapping:
    DEFAULT_IF_IDENTIFIER_NOT_MAPPED = [""]

    def get_substances_mapped(self, identifier: str) -> List[str]:
        pass
