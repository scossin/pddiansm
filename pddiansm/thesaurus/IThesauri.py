from typing import List

from pddiansm.thesaurus.IThesaurus import IThesaurus


class IThesauri:
    """
    This class stores all thesaurus instances
    """

    def get_thesaurus(self, thesaurus_version) -> IThesaurus:
        pass

    def get_available_thesaurus_version(self) -> List[str]:
        pass

    def print_available_thesaurus_version(self) -> None:
        for version in self.get_available_thesaurus_version():
            print(version)
