from pathlib import Path
from typing import List
import os
import pydantic

from pddiansm.pddiansm.thesaurus.ThesaurusExceptions import ThesaurusVersionNotFound
from pddiansm.pddiansm.interfaces.interfaces_pddi import PDDI
from pddiansm.pddiansm.thesaurus.versions import Version, THESAURUS_VERSIONS
from pddiansm.pddiansm.utils.normalize_string import normalize_string


class Thesaurus:
    instances: {str: List[PDDI]} = None

    def __init__(self):
        raise TypeError("Cannot create 'Thesaurus' instances, access this class statically")

    @classmethod
    def get_version(cls, version: THESAURUS_VERSIONS) -> List[PDDI]:
        Thesaurus.__initialize()
        if version.name not in Thesaurus.instances:
            raise ThesaurusVersionNotFound(f"Thesaurus version {version.name} was not found")
        return Thesaurus.instances[version.name]

    @classmethod
    def __initialize(cls):
        if not Thesaurus.instances:
            Thesaurus.instances = {}
            for version in THESAURUS_VERSIONS:
                Thesaurus.instances[version.name] = Thesaurus.__load_version(version)

    @classmethod
    def __load_version(cls, version: Version) -> List[PDDI]:
        current_dir = os.path.dirname(__file__)
        path = Path(current_dir + "/" + version.thesaurus_file)
        pddis = pydantic.parse_file_as(List[PDDI], path)
        Thesaurus.__normalize_pddis(pddis)
        return tuple(pddis)

    @classmethod
    def __normalize_pddis(cls, pddis):
        for pddi in pddis:
            pddi.plus_drug = normalize_string(pddi.plus_drug)
            pddi.main_drug = normalize_string(pddi.main_drug)
