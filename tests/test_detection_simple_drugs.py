import unittest
from typing import List

import pydantic

from pddiansm.detector.PDDIansmDetectorSimpleDrugs import PDDIansmDetectorSimpleDrugs
from pddiansm.detector.PDDIdrugsDetected import PDDIdrugsDetected
from pddiansm.interfaces.interfaces_input import SimpleDrug
from pddiansm.thesaurus.Thesauri import Thesauri
from tests.test_interfaces import get_path


def get_pddi_detector_2019():
    thesaurus = Thesauri().get_thesaurus("2019_09")
    pddi_detector = PDDIansmDetectorSimpleDrugs(thesaurus)
    return pddi_detector


class MyTestCase(unittest.TestCase):
    def test_detection_simple_drugs(self):
        # the PDDI detector
        pddi_detector = get_pddi_detector_2019()
        # load a patient_drugs object
        path = get_path("../pddiansm/interfaces/simple_drugs_test.json")
        patient_drugs = pydantic.parse_file_as(List[SimpleDrug], path)
        # PDDIs detection
        pddis: List[PDDIdrugsDetected] = pddi_detector.detect_pddi_simple_drugs(patient_drugs)
        self.assertEqual(len(pddis), 1)

    def test_detection_patient_drugs_no_pddi(self):
        # the PDDI detector
        pddi_detector = get_pddi_detector_2019()
        # load a simple_drugs object
        path = get_path("../pddiansm/interfaces/simple_drugs_test.json")
        simple_drugs: List[SimpleDrug] = pydantic.parse_file_as(List[SimpleDrug], path)
        # change the first substance
        simple_drugs[0].substances[0].substance = "opium"
        # PDDIs detection
        pddis: List[PDDIdrugsDetected] = pddi_detector.detect_pddi_simple_drugs(simple_drugs)
        self.assertEqual(len(pddis), 0)


if __name__ == '__main__':
    unittest.main()
