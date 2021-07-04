import unittest
from typing import List

import pydantic

from pddiansm.detector.PDDIansmDetectorSimpleDrugs import PDDIansmDetectorSimpleDrugs
from pddiansm.detector.PDDIsimpleDrugsDetected import PDDIsimpleDrugsDetected
from pddiansm.pydantic.interfaces_input import SimpleDrug
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.ThesauriJson import ThesauriJson
from tests.test_interfaces import get_path


def get_pddi_detector_2019():
    thesaurus: IThesaurus = ThesauriJson().get_thesaurus("2019_09")
    pddi_detector = PDDIansmDetectorSimpleDrugs(thesaurus)
    return pddi_detector


def get_simple_drugs_example():
    # load a simple_drugs object
    path = get_path("../pddiansm/pydantic/simple_drugs_test.json")
    simple_drugs = pydantic.parse_file_as(List[SimpleDrug], path)
    return simple_drugs


class MyTestCase(unittest.TestCase):
    def test_detection_simple_drugs(self):
        pddi_detector = get_pddi_detector_2019()
        simple_drugs = get_simple_drugs_example()
        pddis: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        self.assertEqual(len(pddis), 1)

    def test_detection_print(self):
        pddi_detector = get_pddi_detector_2019()
        simple_drugs = get_simple_drugs_example()
        pddis: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        expected_string = "azithromycine (from 'macrolides (sauf spiramycine)') can interact with colchicine (from 'colchicine') in thesaurus version 2019_09" \
                          "\nazithromycine comes from drug number '1' and colchicine comes from drug number '2'"
        pddi_1 = pddis[0]
        message_pddi_1 = pddi_1.__str__()
        self.assertEqual(message_pddi_1, expected_string)

    def test_detection_patient_drugs_no_pddi(self):
        # the PDDI detector
        pddi_detector = get_pddi_detector_2019()
        # load a simple_drugs object
        path = get_path("../pddiansm/pydantic/simple_drugs_test.json")
        simple_drugs: List[SimpleDrug] = pydantic.parse_file_as(List[SimpleDrug], path)
        # change the first substance
        simple_drugs[0].substances[0].substance = "opium"
        # PDDIs detection
        pddis: List[PDDIsimpleDrugsDetected] = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
        self.assertEqual(len(pddis), 0)


if __name__ == '__main__':
    unittest.main()
