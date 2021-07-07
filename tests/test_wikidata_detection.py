import unittest
from typing import List

import pydantic

from pddiansm.detected.PDDIdetected import PDDIdetected
from pddiansm.detected.PDDIsimpleDrugsDetected import PDDIsimpleDrugsDetected
from pddiansm.mapper.AvailableIdentifierMappers import AvailableSubstanceMapping
from tests.test_detection import get_pddi_thesaurus_detector_2019
from pddiansm.pydantic.interfaces_input import SimpleDrug
from tests.test_detection_simple_drugs import get_pddi_simple_drugs_detector_2019
from tests.test_interfaces import get_path


def get_simple_drugs_example():
    # load a simple_drugs object
    path = get_path("data/simple_drugs_wikidata_test.json")
    simple_drugs = pydantic.parse_file_as(List[SimpleDrug], path)
    return simple_drugs


def set_wikidata_mapper(pddi_detector):
    wikidata_mapper = AvailableSubstanceMapping.Wikidata.value
    pddi_detector.set_mapper(wikidata_mapper)


class MyTestCase(unittest.TestCase):
    def test_detection_2_substances(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        set_wikidata_mapper(pddi_detector)
        identifier_domperidone = "Q424238"
        identifier_escitalopram = "Q423757"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(identifier_domperidone, identifier_escitalopram)
        self.assertTrue(len(pddis_detected) == 1)

    def test_mocs_belong_to_plus_and_main_drugs(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        set_wikidata_mapper(pddi_detector)
        identifier_domperidone = "Q424238"
        identifier_escitalopram = "Q423757"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(identifier_domperidone, identifier_escitalopram)
        pddi0 = pddis_detected[0]
        self.assertTrue(pddi0.mocs_belong_to_plus_and_main_drugs)

    def test_detection_simple_drugs_wikidata(self):
        pddi_detector = get_pddi_simple_drugs_detector_2019()
        set_wikidata_mapper(pddi_detector)
        simple_drugs = get_simple_drugs_example()
        pddis: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        self.assertEqual(len(pddis), 1)


if __name__ == '__main__':
    unittest.main()
