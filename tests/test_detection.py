import unittest
from typing import List

from pddiansm.detector.PDDIthesaurusDetector import PDDIthesaurusDetector
from pddiansm.detected.PDDIdetected import PDDIdetected
from pddiansm.pydantic.interfaces_pddi import PDDI
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.ThesauriJson import ThesauriJson


def get_thesaurus_2009() -> IThesaurus:
    thesaurus = ThesauriJson().get_thesaurus("2019_09")
    return thesaurus


def get_pddi_thesaurus_detector_2019():
    thesaurus: IThesaurus = get_thesaurus_2009()
    pddi_detector = PDDIthesaurusDetector(thesaurus)
    return pddi_detector


class MyTestCase(unittest.TestCase):
    def test_detection_commutativity(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        molecule = "ABATACEPT"
        classe = "ANTI-TNF ALPHA"
        pddi0: PDDI = pddi_detector._search_pddi_in_index(molecule, classe)
        pddi1: PDDI = pddi_detector._search_pddi_in_index(classe, molecule)
        self.assertEqual(pddi0, pddi1)

    def test_detection_substance_classe(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "abatacept"
        classe1 = "anti-tnf alpha"
        pddis: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, classe1)
        self.assertTrue(len(pddis) == 1)

    def test_pddi_detected_equality(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
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
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "abatacept"
        substance2 = "a molecule that doesn't exist"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 0)

    def test_detection_classe_classe(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        classe1 = "Minéralocorticoïdes"
        classe2 = "Anticonvulsivants Inducteurs enzymatiques"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(classe1, classe2)
        self.assertTrue(len(pddis_detected) == 1)

    def test_detection_substance_substance(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "dompéridone"
        substance2 = "escitalopram"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 1)

    def test_mocs_belong_to_plus_and_main_drugs(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "dompéridone"
        substance2 = "escitalopram"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        pddi0 = pddis_detected[0]
        self.assertTrue(pddi0.mocs_belong_to_plus_and_main_drugs)

    def test_print_when_mocs_belong_to_plus_and_main_drugs(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "dompéridone"
        substance2 = "escitalopram"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        pddi0 = pddis_detected[0]
        self.assertTrue(pddi0.__str__(),
                        f"dompéridone(or escitalopram) (from 'substances susceptibles de donner des torsades de pointes') can interact "
                        f"with escitalopram(or dompéridone) (from 'torsadogenes (sauf arsenieux, antiparasitaires, neuroleptiques, methadone...)') "
                        f"in thesaurus version 2019_09")

        substance1 = "escitalopram"
        substance2 = "dompéridone"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        pddi0 = pddis_detected[0]
        self.assertTrue(pddi0.__str__(),
                        f"escitalopram(or dompéridone) (from 'substances susceptibles de donner des torsades de pointes') can interact "
                        f"with dompéridone(or escitalopram) (from 'torsadogenes (sauf arsenieux, antiparasitaires, neuroleptiques, methadone...)') "
                        f"in thesaurus version 2019_09")

    def test_detection_substance_substance_2(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "azithromycine"
        substance2 = "colchicine"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 1)

    def test_detection_two_codeine(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "codeine"
        substance2 = "codeine"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis_detected) == 3)

    def test_as_dict(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        substance1 = "codeine"
        substance2 = "codeine"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(substance1, substance2)
        pddis_dict = [pddi_detected.as_dict() for pddi_detected in pddis_detected]
        self.assertTrue(len(pddis_dict) == 3)

if __name__ == '__main__':
    unittest.main()
