from typing import List


class IMapper:
    DEFAULT_IF_IDENTIFIER_NOT_MAPPED = [""]

    def get_mocs_mapped(self, identifier: str) -> List[str]:
        """

        :param identifier: an identifier that is mapped to molecule(s) / drug_classe(s)
        :return: substance(s) or drug_class(es) to be searched
        """
        pass
