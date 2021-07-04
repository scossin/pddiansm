import unittest
from typing import List

from pddiansm.detector.PDDIthesaurusDetector import PDDIthesaurusDetector
from pddiansm.detector.PDDIdetected import PDDIdetected
from pddiansm.pydantic.interfaces_pddi import PDDI
from pddiansm.thesaurus.ThesauriJson import ThesauriJson


def get_pddi_detector_2019():
    thesaurus = ThesauriJson().get_thesaurus("2019_09")
    pddi_detector = PDDIthesaurusDetector(thesaurus)
    return pddi_detector


class MyTestCase(unittest.TestCase):
    def test_detection_commutativity(self):
        pddi_detector = get_pddi_detector_2019()
        molecule = "ABATACEPT"
        classe = "ANTI-TNF ALPHA"
        pddi0: PDDI = pddi_detector._search_pddi_in_index(molecule, classe)
        pddi1: PDDI = pddi_detector._search_pddi_in_index(classe, molecule)
        self.assertEqual(pddi0, pddi1)

    def test_detection_substance_classe(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "abatacept"
        classe1 = "anti-tnf alpha"
        pddis: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, classe1)
        self.assertTrue(len(pddis) == 1)

    def test_pddi_detected_equality(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "abatacept"
        classe1 = "anti-tnf alpha"
        pddis: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, classe1)
        pddi_detected_1 = pddis[0]
        pddis: List[PDDIdetected] = pddi_detector.detect_pddi(classe1, substance1)
        pddi_detected_2 = pddis[0]
        self.assertEqual(pddi_detected_1, pddi_detected_2)
        pddi_detected = pddi_detector._remove_duplicates([pddi_detected_1, pddi_detected_2])
        self.assertTrue(len(pddi_detected) == 1)

    def test_detection_when_substance_is_unknown(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "abatacept"
        substance2 = "a molecule that doesn't exist"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 0)

    def test_detection_classe_classe(self):
        pddi_detector = get_pddi_detector_2019()
        classe1 = "Minéralocorticoïdes"
        classe2 = "Anticonvulsivants Inducteurs enzymatiques"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(classe1, classe2)
        self.assertTrue(len(pddis_detected) == 1)

    def test_detection_substance_substance(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "dompéridone"
        substance2 = "escitalopram"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 1)

    def test_detection_substance_substance_2(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "azithromycine"
        substance2 = "colchicine"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 1)

    def test_detection_two_codeine(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "codeine"
        substance2 = "codeine"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 3)


if __name__ == '__main__':
    unittest.main()
