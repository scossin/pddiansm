import os
from pathlib import Path
from typing import List, Union

import pydantic

from pddiansm.pddiansm.thesaurus.ThesaurusExceptions import ThesaurusVersionNotFound
from pddiansm.pddiansm.interfaces.interfaces_pddi import SubstanceThesaurus, ClassThesaurus, SubstanceClasses
from pddiansm.pddiansm.thesaurus.versions import THESAURUS_VERSIONS, Version
from pddiansm.pddiansm.utils.normalize_string import normalize_string


class Substances:
    instances: {str: SubstanceClasses} = None

    def __init__(self):
        raise TypeError("Cannot create 'Substances' instances, access this class statically")

    @classmethod
    def get_version(cls, version: THESAURUS_VERSIONS) -> SubstanceClasses:
        Substances.__initialize()
        if version.name not in Substances.instances:
            raise ThesaurusVersionNotFound(f"Thesaurus version {version.name} was not found")
        return Substances.instances[version.name]

    @classmethod
    def search_molecule_or_class(cls, version: THESAURUS_VERSIONS, molecule_or_class) -> Union[SubstanceThesaurus, ClassThesaurus]:
        Substances.__initialize()
        substances_classes = Substances.get_version(version)
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

    @classmethod
    def __initialize(cls):
        if not Substances.instances:
            Substances.instances = {}
            for version in THESAURUS_VERSIONS:
                Substances.instances[version.name] = Substances.__load_version(version)

    @classmethod
    def __load_version(cls, version: Version) -> SubstanceClasses:
        current_dir = os.path.dirname(__file__)
        path = Path(current_dir + "/" + version.substance_file)
        substances_classes_list = pydantic.parse_file_as(List[SubstanceThesaurus], path)
        Substances.__normalize_substance_classe(substances_classes_list)
        dict_substances_classes = {substance_classes.substance: substance_classes for substance_classes
                                   in substances_classes_list}
        classes = Substances.__get_unique_classes(substances_classes_list)
        substance_classes = SubstanceClasses(hashmap_substances=dict_substances_classes,
                                             classes=classes)
        return substance_classes

    @classmethod
    def __get_unique_classes(cls, substances: List[SubstanceThesaurus]):
        classes_list = [substance.drug_classes for substance in substances]
        flat_classes_list = [classe for sublist in classes_list for classe in sublist]
        unique_classes = set(flat_classes_list)
        return unique_classes

    @classmethod
    def __get_unique_substances(cls, substances: List[SubstanceThesaurus]):
        substances_list = [substance.substance for substance in substances]
        unique_substances = set(substances_list)
        return unique_substances

    @classmethod
    def __normalize_substance_classe(cls, substances_classes_list: List[SubstanceThesaurus]):
        for substance_classes in substances_classes_list:
            substance_classes.substance = normalize_string(substance_classes.substance)
            substance_classes.drug_classes = list(map(normalize_string, substance_classes.drug_classes))

