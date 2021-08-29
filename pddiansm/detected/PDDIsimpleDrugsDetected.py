from typing import Dict

from pddiansm.detected.PDDIdetected import PDDIdetected
from pddiansm.pydantic.interfaces_input import SimpleDrug


class PDDIsimpleDrugsDetected:
    def __init__(self, pddi_detected: PDDIdetected, drug1: SimpleDrug, drug2: SimpleDrug):
        """
        A pddi detected between one substance of drug1 and another substance of drug2
        :param pddi_detected: a potential drug drug interaction
        :param drug1: the first drug that interacts
        :param drug2: the second drug that interacts
        """
        self.pddi_detected: PDDIdetected = pddi_detected
        self.drug1: SimpleDrug = drug1
        self.drug2: SimpleDrug = drug2

    def as_dict(self) -> Dict:
        """
        Get a dictionary representation of the PDDI detected between two simple drugs
        :return: Information about the PDDIdetected and drug_id_1 / drug_id_2
        :rtype: a dictionary
        """
        dict_simple_drugs = self.pddi_detected.as_dict()
        dict_simple_drugs["drug_id_1"] = self.drug1.id
        dict_simple_drugs["drug_id_2"] = self.drug2.id
        return dict_simple_drugs

    def __str__(self):
        print_pddi_detected = self.pddi_detected.__str__()
        substance1 = self.pddi_detected.moc1
        substance2 = self.pddi_detected.moc2
        message = f"{substance1} comes from drug number '{self.drug1.id}' and {substance2} comes from drug number '{self.drug2.id}'"
        return print_pddi_detected + "\n" + message
