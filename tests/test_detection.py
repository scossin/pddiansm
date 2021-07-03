import unittest

from pddiansm.detector.PDDIansmDetector import PDDIansmDetector
from pddiansm.thesaurus.Thesauri import Thesauri


def get_pddi_detector_2019():
    thesaurus = Thesauri().get_thesaurus("2019_09")
    pddi_detector = PDDIansmDetector(thesaurus)
    return pddi_detector


class MyTestCase(unittest.TestCase):
    def test_detection_commutativity(self):
        pddi_detector = get_pddi_detector_2019()
        molecule = "ABATACEPT"
        classe = "ANTI-TNF ALPHA"
        pddi0 = pddi_detector._search_pddi_in_index(molecule, classe)
        pddi1 = pddi_detector._search_pddi_in_index(classe, molecule)
        self.assertEqual(pddi0, pddi1)

    def test_detection_substance_classe(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "abatacept"
        classe1 = "anti-tnf alpha"
        pddis = pddi_detector.detect_pddi(substance1, classe1)
        self.assertTrue(len(pddis) == 1)

    def test_detection_when_substance_is_unknown(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "abatacept"
        substance2 = "a molecule that doesn't exist"
        pddis = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis) == 0)

    def test_detection_classe_classe(self):
        pddi_detector = get_pddi_detector_2019()
        classe1 = "Minéralocorticoïdes"
        classe2 = "Anticonvulsivants Inducteurs enzymatiques"
        pddis = pddi_detector.detect_pddi(classe1, classe2)
        self.assertTrue(len(pddis) == 1)

    def test_detection_substance_substance(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "dompéridone"
        substance2 = "escitalopram"
        pddis = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis) == 2)

    def test_detection_substance_substance_2(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "azithromycine"
        substance2 = "colchicine"
        pddis = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis) == 1)

    def test_detection_ansmDetector(self):
        pddi_detector = get_pddi_detector_2019()
        substance1 = "azithromycine"
        substance2 = "colchicine"
        pddis = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis) == 1)


if __name__ == '__main__':
    unittest.main()
