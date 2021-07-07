from typing import List, Dict

import pydantic

from pddiansm.pydantic.interfaces_pddi import PDDI, SubstanceThesaurus
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.ThesaurusFiles import ThesaurusFiles
from pddiansm.utils.normalize_string import normalize_string


class ThesaurusJson(IThesaurus):
    def __init__(self, thesaurus_files: ThesaurusFiles):
        self.thesaurus_files = thesaurus_files

        thesaurus_file = thesaurus_files.get_thesaurus_file_path()
        self.pddis: List[PDDI] = ThesaurusJson.load_pddis(thesaurus_file)

        substance_file = thesaurus_files.get_substance_file_path()
        self.substances_thesaurus: List[SubstanceThesaurus] = ThesaurusJson.load_substances(substance_file)

    def get_pddis(self) -> List[PDDI]:
        """ Overrides """
        return self.pddis

    def get_substances_thesaurus(self) -> List[SubstanceThesaurus]:
        """ Overrides """
        return self.substances_thesaurus

    def get_thesaurus_version(self) -> str:
        """ Overrides """
        return self.thesaurus_files.thesaurus_version

    def substance_belongs_to_drug_class(self, substance: str, drug_class: str) -> bool:
        """ Overrides """
        substances_of_drug_class = self.map_drug_classes_2_substances.get(drug_class, [])
        normalized_substance = normalize_string(substance)
        return normalized_substance in substances_of_drug_class

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
