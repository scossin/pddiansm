from typing import List

from pddiansm.detector.PDDIansmDetector import PDDIansmDetector
from pddiansm.detector.PDDIsimpleDrugsDetected import PDDIsimpleDrugsDetected
from pddiansm.interfaces.interfaces_input import SimpleDrug
from pddiansm.interfaces.interfaces_pddi import PDDI
from pddiansm.thesaurus.Thesaurus import Thesaurus


class PDDIansmDetectorSimpleDrugs(PDDIansmDetector):
    """
    Detect PDDIs in a list of SimpleDrug. Each simpleDrug can contain one or multiple substances
    """
    def __init__(self, thesaurus: Thesaurus):
        super().__init__(thesaurus)

    def detect_pddi_simple_drugs(self, drugs: List[SimpleDrug]):
        # O(n!): if the patients take 6 drugs, we will have 6x5x4x3x2 = 720 comparisons
        pddis: List[List[PDDIsimpleDrugsDetected]] = [self.detect_pddi_in_drugs(drug1, drug2)
                                                      for drug1 in drugs
                                                      for drug2 in drugs
                                                      if drug1.id < drug2.id]
        pddis_flat: List[PDDIsimpleDrugsDetected] = [pddi for sublist in pddis for pddi in sublist]
        return pddis_flat

    def detect_pddi_in_drugs(self, drug1: SimpleDrug, drug2: SimpleDrug) -> List[PDDIsimpleDrugsDetected]:
        # O(n!): if one drug has 3 substances and the other 2 substances, there are eventually 3*2 = 6 pddis
        pddis_drug_detected: List[PDDIsimpleDrugsDetected] = []
        for i_1, substance_dosage1 in enumerate(drug1.substances):
            for i_2, substance_dosage2 in enumerate(drug2.substances):
                pddis = self.detect_pddi(substance_dosage1.substance, substance_dosage2.substance)
                self.__add_pddis_detected(pddis_drug_detected, pddis, drug1, drug2, i_1, i_2)
        return pddis_drug_detected

    @staticmethod
    def __add_pddis_detected(pddis_drug_detected: List[PDDIsimpleDrugsDetected], pddis: List[PDDI],
                             drug1: SimpleDrug, drug2: SimpleDrug,
                             i_1: int, i_2: int):
        if len(pddis) != 0:
            for pddi in pddis:
                pddi_drug_detected = PDDIsimpleDrugsDetected(pddi, drug1, drug2, i_1, i_2)
                pddis_drug_detected.append(pddi_drug_detected)
