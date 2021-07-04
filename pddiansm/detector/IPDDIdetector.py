from typing import List

from pddiansm.detector.PDDIdetected import PDDIdetected


class IPDDIdetector:

    def detect_pddi(self, string1: str, string2: str) -> List[PDDIdetected]:
        """
        Detect Potential Drug Drug Interaction (PDDI)
        :param string1: a molecule, drug_class, or identifier
        :param string2: a molecule, drug_class, or identifier
        """
        pass

