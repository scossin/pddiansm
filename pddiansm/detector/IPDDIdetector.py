from typing import List

from pddiansm.detected.PDDIdetected import PDDIdetected


class IPDDIdetector:

    def detect_pddi(self, string1: str, string2: str) -> List[PDDIdetected]:
        """
        Detect all Potential Drug Drug Interactions (PDDIs) according to the ANSM guidelines document
        from two molecules or classes in string format
        :param string1: a molecule, a drug class or an identifier
        :param string2: a molecule, a drug class or an identifier
        :return: a List of PDDIs detected
        """
        pass

