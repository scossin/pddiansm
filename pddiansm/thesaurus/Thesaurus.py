from typing import List

import pydantic

from pddiansm.interfaces.interfaces_pddi import PDDI, SubstanceThesaurus
from pddiansm.thesaurus.ThesaurusFiles import ThesaurusFiles
from pddiansm.utils.normalize_string import normalize_string


class Thesaurus:
    """
    This class stores the content of a thesaurus:
        - PDDIs: list of potential drug drug interactions
        - substances_thesaurus: list of substances and their classes
    """

    def __init__(self, thesaurus_files: ThesaurusFiles):
        self.thesaurus_files = thesaurus_files

        thesaurus_file = thesaurus_files.get_thesaurus_file_path()
        self.pddis: List[PDDI] = Thesaurus.load_pddis(thesaurus_file)

        substance_file = thesaurus_files.get_substance_file_path()
        self.substances_thesaurus: List[SubstanceThesaurus] = Thesaurus.load_substances(substance_file)

    def get_unique_substances(self):
        substances_list = [substance_thesaurus.substance for substance_thesaurus in self.substances_thesaurus]
        unique_substances = set(substances_list)
        return unique_substances

    def get_unique_drug_classes(self):
        classes_list = [substance_thesaurus.drug_classes for substance_thesaurus in self.substances_thesaurus]
        flat_classes_list = [classe for sublist in classes_list for classe in sublist]
        unique_classes = set(flat_classes_list)
        return unique_classes

    @classmethod
    def load_pddis(cls, thesaurus_file: str) -> List[PDDI]:
        pddis = pydantic.parse_file_as(List[PDDI], thesaurus_file)
        cls.__normalize_pddis(pddis)
        return pddis

    @classmethod
    def load_substances(cls, substance_file: str) -> List[SubstanceThesaurus]:
        substances_thesaurus = pydantic.parse_file_as(List[SubstanceThesaurus], substance_file)
        cls.__normalize_substance_thesaurus(substances_thesaurus)
        return substances_thesaurus

    @classmethod
    def __normalize_pddis(cls, pddis):
        for pddi in pddis:
            pddi.plus_drug = normalize_string(pddi.plus_drug)
            pddi.main_drug = normalize_string(pddi.main_drug)

    @classmethod
    def __normalize_substance_thesaurus(cls, substances_thesaurus: List[SubstanceThesaurus]):
        for substance_classes in substances_thesaurus:
            substance_classes.substance = normalize_string(substance_classes.substance)
            substance_classes.drug_classes = list(map(normalize_string, substance_classes.drug_classes))
