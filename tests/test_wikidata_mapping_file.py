import unittest
from typing import List

from pddiansm import pydantic
from pddiansm.mapper.AvailableIdentifierMappers import AvailableSubstanceMapping
from pddiansm.mapper.ISubstanceMapping import ISubstanceMapping


class MyTestCase(unittest.TestCase):
    def test_wikidata_substance_mapping(self):
        substance_mapping = AvailableSubstanceMapping.Wikidata.value
        substance = substance_mapping.get_substances_mapped("Q2697833")
        self.assertEqual(substance, ["abatacept"])
        substance = substance_mapping.get_substances_mapped("Q424238")
        self.assertEqual(substance, ["domperidone"])
        substance = substance_mapping.get_substances_mapped("Q423757")
        self.assertEqual(substance, ["escitalopram"])

    def test_wikidata_substance_mapping_not_found(self):
        substance_mapping = AvailableSubstanceMapping.Wikidata.value
        substance = substance_mapping.get_substances_mapped("identifier_does_not_exist")
        self.assertEqual(substance, ISubstanceMapping.DEFAULT_IF_IDENTIFIER_NOT_MAPPED)


if __name__ == '__main__':
    unittest.main()
