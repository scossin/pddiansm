import unittest
from typing import List

import pydantic

from pddiansm.pddiansm.interfaces.interfaces_input import PatientDrugs
from pddiansm.pddiansm.detector.PDDIansmDetector import PDDIansmDetector
from pddiansm.pddiansm.detector.PDDIansmDetectorDrugs import PDDIansmDetectorDrugs
from pddiansm.pddiansm.detector.PDDIdrugsDetected import PDDIdrugsDetected
from pddiansm.pddiansm.thesaurus.versions import THESAURUS_VERSIONS
from pddiansm.tests.test_interfaces import get_path


class MyTestCase(unittest.TestCase):
    def test_detection_commutativity(self):
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetector(thesaurus_version)
        molecule = "ABATACEPT"
        classe = "ANTI-TNF ALPHA"
        pddi0 = pddi_detector._search_pddi_in_index(molecule, classe)
        pddi1 = pddi_detector._search_pddi_in_index(classe, molecule)
        self.assertEqual(pddi0, pddi1)

    def test_detection_substance_classe(self):
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetector(thesaurus_version)
        substance1 = "abatacept"
        classe1 = "anti-tnf alpha"
        pddis = pddi_detector.detect_pddi(substance1, classe1)
        self.assertTrue(len(pddis) == 1)

    def test_detection_classe_classe(self):
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetector(thesaurus_version)
        classe1 = "Minéralocorticoïdes"
        classe2 = "Anticonvulsivants Inducteurs enzymatiques"
        pddis = pddi_detector.detect_pddi(classe1, classe2)
        self.assertTrue(len(pddis) == 1)

    def test_detection_substance_substance(self):
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetector(thesaurus_version)
        substance1 = "dompéridone"
        substance2 = "escitalopram"
        pddis = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis) == 2)

    def test_detection_substance_substance_2(self):
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetector(thesaurus_version)
        substance1 = "azithromycine"
        substance2 = "colchicine"
        pddis = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis) == 1)

    def test_detection_ansmDetector(self):
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetectorDrugs(thesaurus_version)
        substance1 = "azithromycine"
        substance2 = "colchicine"
        pddis = pddi_detector.detect_pddi(substance1, substance2)
        self.assertTrue(len(pddis) == 1)

    def test_detection_patient_drugs(self):
        # the PDDI detector
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetectorDrugs(thesaurus_version)
        # load a patient_drugs object
        path = get_path("../pddiansm/interfaces/patient_drugs_tests.json")
        patient_drugs = pydantic.parse_file_as(PatientDrugs, path)
        # PDDIs detection
        pddis: List[PDDIdrugsDetected] = pddi_detector.detect_pddi_in_patient_drugs(patient_drugs)
        self.assertEqual(len(pddis), 1)

    def test_detection_patient_drugs_no_pddi(self):
        # the PDDI detector
        thesaurus_version = THESAURUS_VERSIONS[0]
        pddi_detector = PDDIansmDetectorDrugs(thesaurus_version)
        # load a patient_drugs object
        path = get_path("../pddiansm/interfaces/patient_drugs_tests.json")
        patient_drugs: PatientDrugs = pydantic.parse_file_as(PatientDrugs, path)
        # change the first substance
        patient_drugs.drugs[0].substances[0].substance = "opium"
        # PDDIs detection
        pddis: List[PDDIdrugsDetected] = pddi_detector.detect_pddi_in_patient_drugs(patient_drugs)
        self.assertEqual(len(pddis), 0)


if __name__ == '__main__':
    unittest.main()
