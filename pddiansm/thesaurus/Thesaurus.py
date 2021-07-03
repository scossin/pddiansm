from typing import List, Union

import pydantic

from pddiansm.interfaces.interfaces_pddi import PDDI, SubstanceThesaurus, SubstanceClasses, ClassThesaurus
from pddiansm.thesaurus.ThesaurusFiles import ThesaurusFiles
from pddiansm.utils.normalize_string import normalize_string


class Thesaurus:
    def __init__(self, thesaurus_files: ThesaurusFiles):
        self.thesaurus_files = thesaurus_files

        thesaurus_file = thesaurus_files.get_thesaurus_file_path()
        self.pddis: List[PDDI] = Thesaurus.load_pddis(thesaurus_file)

        substance_file = thesaurus_files.get_substance_file_path()
        self.substances_thesaurus: List[SubstanceThesaurus] = Thesaurus.load_substances(substance_file)
        self.substance_classes = self.__create_dict_substances_classes()

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

    def __create_dict_substances_classes(self):
        dict_substances_classes = {substance_classes.substance: substance_classes for substance_classes
                                   in self.substances_thesaurus}
        classes = Thesaurus.__get_unique_classes(self.substances_thesaurus)
        substance_classes = SubstanceClasses(hashmap_substances=dict_substances_classes, classes=classes)
        return substance_classes

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

    def search_molecule_or_class(self, molecule_or_class) -> Union[SubstanceThesaurus, ClassThesaurus]:
        substances_classes = self.substance_classes
        molecule_or_class = normalize_string(molecule_or_class)
        if molecule_or_class in substances_classes.hashmap_substances:
            return substances_classes.hashmap_substances[molecule_or_class]
        elif molecule_or_class in substances_classes.classes:
            return ClassThesaurus(drug_class=molecule_or_class,
                                  substances=[]) # why is it empty when the class contains molecules?
        # when we check PDDI with a class, we don't want to check PDDI for every individual substances that the class contains
        # so we let substances empty to detect PDDI only at the class level
        else:
            return None