import unittest
from typing import List

import pydantic

from pddiansm.detector.PDDIsimpleDrugsDetector import PDDIsimpleDrugsDetector
from pddiansm.detected.PDDIsimpleDrugsDetected import PDDIsimpleDrugsDetected
from pddiansm.pydantic.interfaces_input import SimpleDrug
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.ThesauriJson import ThesauriJson
from tests.test_interfaces import get_path


def get_pddi_simple_drugs_detector_2019():
    thesaurus: IThesaurus = ThesauriJson().get_thesaurus("2019_09")
    pddi_detector = PDDIsimpleDrugsDetector(thesaurus)
    return pddi_detector


def get_simple_drugs_example():
    # load a simple_drugs object
    path = get_path("data/simple_drugs_test.json")
    simple_drugs = pydantic.parse_file_as(List[SimpleDrug], path)
    return simple_drugs


class MyTestCase(unittest.TestCase):
    def test_detection_simple_drugs(self):
        pddi_detector = get_pddi_simple_drugs_detector_2019()
        simple_drugs = get_simple_drugs_example()
        pddis: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        self.assertEqual(len(pddis), 1)

    def test_detection_print(self):
        pddi_detector = get_pddi_simple_drugs_detector_2019()
        simple_drugs = get_simple_drugs_example()
        pddis: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        expected_string = "azithromycine (from 'macrolides (sauf spiramycine)') can interact with colchicine (from 'colchicine') in thesaurus version 2019_09" \
                          "\nazithromycine comes from drug number '1' and colchicine comes from drug number '2'"
        pddi_1 = pddis[0]
        message_pddi_1 = pddi_1.__str__()
        self.assertEqual(message_pddi_1, expected_string)

    def test_detection_patient_drugs_no_pddi(self):
        # the PDDI detector
        pddi_detector = get_pddi_simple_drugs_detector_2019()
        # load a simple_drugs object
        path = get_path("data/simple_drugs_test.json")
        simple_drugs: List[SimpleDrug] = pydantic.parse_file_as(List[SimpleDrug], path)
        # change the first substance
        simple_drugs[0].substances[0] = "opium"
        # PDDIs detection
        pddis: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        self.assertEqual(len(pddis), 0)

    def test_detect_simple_drug_same_drug(self):
        simple_drug1 = SimpleDrug(id=1, substances=["colchicine", "opium", "tiemonium"])
        simple_drug2 = SimpleDrug(id=2, substances=["azithromycine"])
        simple_drugs = [simple_drug1, simple_drug2]
        thesaurus: IThesaurus = ThesauriJson().get_thesaurus("2019_09")
        pddi_detector = PDDIsimpleDrugsDetector(thesaurus)
        pddis_detected: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        [pddi_detected.as_dict() for pddi_detected in pddis_detected]
        self.assertTrue(len(pddis_detected), 1)


if __name__ == '__main__':
    unittest.main()
