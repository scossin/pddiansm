import unittest
from typing import List

from pddiansm.detected.PDDIdetected import PDDIdetected
from pddiansm.mapper.AvailableIdentifierMappers import AvailableSubstanceMapping
from tests.test_detection import get_pddi_thesaurus_detector_2019


def set_rxnorm_mapper(pddi_detector):
    rxnorm_mapper = AvailableSubstanceMapping.RxNorm.value
    pddi_detector.set_mapper(rxnorm_mapper)


class MyTestCase(unittest.TestCase):
    def test_detection_2_substances(self):
        pddi_detector = get_pddi_thesaurus_detector_2019()
        rxnorm_mapper = AvailableSubstanceMapping.RxNorm.value
        pddi_detector.set_mapper(rxnorm_mapper)
        identifier_rxnorm_domperidone = "3626"
        identifier_rxnorm_escitalopram = "321988"
        pddis_detected: List[PDDIdetected] = pddi_detector.detect_pddi(identifier_rxnorm_domperidone,
                                                                       identifier_rxnorm_escitalopram)
        self.assertTrue(len(pddis_detected) == 1)


if __name__ == '__main__':
    unittest.main()
