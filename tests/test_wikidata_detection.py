import unittest
from typing import List

from pddiansm.detector.PDDIdetected import PDDIdetected
from pddiansm.mapper.IdentifierMapper import IdentifierMapper
from tests.test_detection import get_pddi_detector_2019
from tests.test_wikidata_mapping_file import get_wikidata_substance_mapping


class MyTestCase(unittest.TestCase):
    def test_detection_2_substances(self):
        pddi_detector = get_pddi_detector_2019()
        substance_mapping = get_wikidata_substance_mapping()
        string_mapper = pddi_detector.string_mapper
        new_mapper = IdentifierMapper(string_mapper, substance_mapping)
        pddi_detector.set_mapper(new_mapper)
        identifier_domperidone = "Q424238"
        identifier_escitalopram = "Q423757"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(identifier_domperidone, identifier_escitalopram)
        self.assertTrue(len(pddis_detected) == 1)


if __name__ == '__main__':
    unittest.main()
