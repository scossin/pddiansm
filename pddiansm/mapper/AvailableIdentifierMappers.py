import enum
import importlib.resources as pkg_resources

from pddiansm.mapper.IMapper import IMapper
from pddiansm.mapper.MappingFile import MappingFile


def get_package_mapping_file(filename) -> str:
    package_path = pkg_resources.path("pddiansm", "data")
    with package_path as path:
        filepath = str(path) + "/mappings/" + filename
        return filepath


def get_wikidata_mapping() -> IMapper:
    filename = "wikidata_mappings.tsv"
    wikidata_file = get_package_mapping_file(filename)
    wikipedia_mapping: IMapper = MappingFile(wikidata_file)
    return wikipedia_mapping


def get_rxnorm_mapping() -> IMapper:
    filename = "rxnorm_mappings.tsv"
    rxnorm_file = get_package_mapping_file(filename)
    wikipedia_mapping: IMapper = MappingFile(rxnorm_file)
    return wikipedia_mapping


class AvailableSubstanceMapping(enum.Enum):
    Wikidata = get_wikidata_mapping()
    RxNorm = get_rxnorm_mapping()
