import unittest

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


class MyTestCase(unittest.TestCase):
    def test_wikidata_substance_mapping(self):
        substance_mapping = get_wikidata_substance_mapping()
        substance = substance_mapping.get_substances_mapped("Q2697833")
        self.assertEqual(substance, ["abatacept"])
        substance = substance_mapping.get_substances_mapped("Q424238")
        self.assertEqual(substance, ["domperidone"])
        substance = substance_mapping.get_substances_mapped("Q423757")
        self.assertEqual(substance, ["escitalopram"])

    def test_wikidata_substance_mapping_not_found(self):
        substance_mapping = get_wikidata_substance_mapping()
        substance = substance_mapping.get_substances_mapped("identifier_does_not_exist")
        self.assertEqual(substance, ISubstanceMapping.DEFAULT_IF_IDENTIFIER_NOT_MAPPED)


if __name__ == '__main__':
    unittest.main()
