from typing import List, Union

import pydantic

from pddiansm.interfaces.interfaces_pddi import PDDI, SubstanceThesaurus, SubstanceClasses, ClassThesaurus
from pddiansm.thesaurus.ThesaurusFiles import ThesaurusFiles
from pddiansm.utils.normalize_string import normalize_string


class Thesaurus:
    """
    This class stores the content of a thesaurus:
        - PDDIs: list of potential drug drug interactions
        - substance_thesaurus: list of substances and their classes
    """

    def __init__(self, thesaurus_files: ThesaurusFiles):
        self.thesaurus_files = thesaurus_files

        thesaurus_file = thesaurus_files.get_thesaurus_file_path()
        self.pddis: List[PDDI] = Thesaurus.load_pddis(thesaurus_file)

        substance_file = thesaurus_files.get_substance_file_path()
        self.substances_thesaurus: List[SubstanceThesaurus] = Thesaurus.load_substances(substance_file)
        self.substances_and_classes = self.__create_dict_substances_classes(self.substances_thesaurus)

    def search_molecule_or_class(self, molecule_or_class: str) -> Union[SubstanceThesaurus, ClassThesaurus]:
        substances_classes = self.substances_and_classes
        molecule_or_class = normalize_string(molecule_or_class)
        if molecule_or_class in substances_classes.hashmap_substances:
            return substances_classes.hashmap_substances[molecule_or_class]
        elif molecule_or_class in substances_classes.hashmap_drug_classes:
            return substances_classes.hashmap_drug_classes[molecule_or_class]
        else:
            return None

    @classmethod
    def load_pddis(cls, thesaurus_file: str) -> List[PDDI]:
        pddis = pydantic.parse_file_as(List[PDDI], thesaurus_file)
        cls.__normalize_pddis(pddis)
        return pddis

    @classmethod
    def load_substances(cls, substance_file: str) -> List[SubstanceThesaurus]:
        substances_thesaurus = pydantic.parse_file_as(List[SubstanceThesaurus], substance_file)
        cls.__normalize_substance_classe(substances_thesaurus)
        return substances_thesaurus

    @staticmethod
    def __create_dict_substances_classes(substances_thesaurus) -> SubstanceClasses:
        dict_substances_classes = {substance_classes.substance: substance_classes for substance_classes
                                   in substances_thesaurus}
        drug_classes = Thesaurus.__get_unique_classes(substances_thesaurus)

        dict_drug_classes = {drug_class: ClassThesaurus(drug_class=drug_class,
                                                        substances=[]) for drug_class in drug_classes}
        # why substances=[] if the class contains molecules?
        # when we check PDDI with a class, we don't want to check PDDI for every individual substances that the class contains
        # so we let substances empty to detect PDDI only at the class level

        substances_and_classes = SubstanceClasses(hashmap_substances=dict_substances_classes,
                                                  hashmap_drug_classes=dict_drug_classes)
        return substances_and_classes

    @classmethod
    def __normalize_pddis(cls, pddis):
        for pddi in pddis:
            pddi.plus_drug = normalize_string(pddi.plus_drug)
            pddi.main_drug = normalize_string(pddi.main_drug)

    @classmethod
    def __normalize_substance_classe(cls, substances_thesaurus: List[SubstanceThesaurus]):
        for substance_classes in substances_thesaurus:
            substance_classes.substance = normalize_string(substance_classes.substance)
            substance_classes.drug_classes = list(map(normalize_string, substance_classes.drug_classes))

    @classmethod
    def __get_unique_substances(cls, substances: List[SubstanceThesaurus]):
        substances_list = [substance.substance for substance in substances]
        unique_substances = set(substances_list)
        return unique_substances

    @classmethod
    def __get_unique_classes(cls, substances: List[SubstanceThesaurus]):
        classes_list = [substance.drug_classes for substance in substances]
        flat_classes_list = [classe for sublist in classes_list for classe in sublist]
        unique_classes = set(flat_classes_list)
        return unique_classes
