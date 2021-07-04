from typing import List

from pddiansm.detector.PDDIthesaurusDetector import PDDIthesaurusDetector
from pddiansm.detector.PDDIdetected import PDDIdetected
from pddiansm.detector.PDDIsimpleDrugsDetected import PDDIsimpleDrugsDetected
from pddiansm.pydantic.interfaces_input import SimpleDrug
from pddiansm.thesaurus.IThesaurus import IThesaurus


class PDDIansmDetectorSimpleDrugs(PDDIthesaurusDetector):
    """
    Detect PDDIs in a list of SimpleDrug. Each simpleDrug can contain one or multiple substances
    """
    def __init__(self, thesaurus: IThesaurus):
        super().__init__(thesaurus)

    def detect_pddi_multiple_drugs(self, drugs: List[SimpleDrug]) -> List[PDDIsimpleDrugsDetected]:
        # O(n!): if the patients take 6 drugs, we will have 6x5x4x3x2 = 720 comparisons
        pddis: List[List[PDDIsimpleDrugsDetected]] = [self.detect_pddi_two_drugs(drug1, drug2)
                                                      for drug1 in drugs
                                                      for drug2 in drugs
                                                      if drug1.id < drug2.id]
        pddis_flat: List[PDDIsimpleDrugsDetected] = [pddi for sublist in pddis for pddi in sublist]
        return pddis_flat

    def detect_pddi_two_drugs(self, drug1: SimpleDrug, drug2: SimpleDrug) -> List[PDDIsimpleDrugsDetected]:
        # O(n!): if one drug has 3 substances and the other 2 substances, there are eventually 3*2 = 6 pddis
        pddis_drug_detected: List[PDDIsimpleDrugsDetected] = []
        for i_1, substance_dosage1 in enumerate(drug1.substances):
            for i_2, substance_dosage2 in enumerate(drug2.substances):
                pddis_detected: List[PDDIdetected] = self.detect_pddi(substance_dosage1.substance,
                                                                      substance_dosage2.substance)
                self.__add_pddis_detected(pddis_drug_detected, pddis_detected, drug1, drug2)
        return pddis_drug_detected

    @staticmethod
    def __add_pddis_detected(pddis_drug_detected: List[PDDIsimpleDrugsDetected], pddis_detected: List[PDDIdetected],
                             drug1: SimpleDrug, drug2: SimpleDrug):
        if len(pddis_detected) != 0:
            for pddi_detected in pddis_detected:
                pddi_drug_detected = PDDIsimpleDrugsDetected(pddi_detected, drug1, drug2)
                pddis_drug_detected.append(pddi_drug_detected)
