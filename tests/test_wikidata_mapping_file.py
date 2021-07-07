import unittest

from pddiansm.mapper.AvailableIdentifierMappers import AvailableSubstanceMapping
from pddiansm.mapper.IMapper import IMapper


class MyTestCase(unittest.TestCase):
    def test_wikidata_substance_mapping(self):
        substance_mapping = AvailableSubstanceMapping.Wikidata.value
        substance = substance_mapping.get_mocs_mapped("Q2697833")
        self.assertEqual(substance, ["abatacept"])
        substance = substance_mapping.get_mocs_mapped("Q424238")
        self.assertEqual(substance, ["domperidone"])
        substance = substance_mapping.get_mocs_mapped("Q423757")
        self.assertEqual(substance, ["escitalopram"])

    def test_wikidata_substance_mapping_not_found(self):
        substance_mapping = AvailableSubstanceMapping.Wikidata.value
        substance = substance_mapping.get_mocs_mapped("identifier_does_not_exist")
        self.assertEqual(substance, IMapper.DEFAULT_IF_IDENTIFIER_NOT_MAPPED)


if __name__ == '__main__':
    unittest.main()
