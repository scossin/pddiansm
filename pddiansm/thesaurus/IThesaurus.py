from typing import List

from pddiansm.pydantic.interfaces_pddi import PDDI, SubstanceThesaurus


class IThesaurus:
    """
    This class stores the content of a thesaurus:
        - PDDIs: list of potential drug drug interactions
        - substances_thesaurus: list of substances and their classes
    """

    def get_pddis(self) -> List[PDDI]:
        pass

    def get_substances_thesaurus(self) -> List[SubstanceThesaurus]:
        pass

    def get_thesaurus_version(self) -> str:
        pass

    def get_unique_substances(self):
        substances_list = [substance_thesaurus.substance for substance_thesaurus in self.get_substances_thesaurus()]
        unique_substances = set(substances_list)
        return unique_substances

    def get_unique_drug_classes(self):
        classes_list = [substance_thesaurus.drug_classes for substance_thesaurus in self.get_substances_thesaurus()]
        flat_classes_list = [classe for sublist in classes_list for classe in sublist]
        unique_classes = set(flat_classes_list)
        return unique_classes
