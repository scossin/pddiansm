import enum
import importlib.resources as pkg_resources

from pddiansm.mapper.ISubstanceMapping import ISubstanceMapping
from pddiansm.mapper.SubstanceMappingFile import SubstanceMappingFile


def get_wikidata_file() -> str:
    package_path = pkg_resources.path("pddiansm", "data")
    with package_path as path:
        filepath = str(path) + "/mappings/ansm_substances_mappings.tsv"
        return filepath


def get_wikidata_substance_mapping() -> ISubstanceMapping:
    wikidata_file = get_wikidata_file()
    substance_mapping: ISubstanceMapping = SubstanceMappingFile(wikidata_file)
    return substance_mapping


class AvailableSubstanceMapping(enum.Enum):
    Wikidata = get_wikidata_substance_mapping()
