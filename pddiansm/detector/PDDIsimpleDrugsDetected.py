from pddiansm.detector.PDDIdetected import PDDIdetected
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

    def get_dict_representation(self):
        return {
            "drug_id_1": self.drug1.id,
            "drug_id_2": self.drug2.id,
            "pddi": self.pddi_detected.get_dict_representation_pddi()
        }

    def __str__(self):
        print_pddi_detected = self.pddi_detected.__str__()
        substance1 = self.pddi_detected.moc1
        substance2 = self.pddi_detected.moc2
        message = f"{substance1} comes from drug number '{self.drug1.id}' and {substance2} comes from drug number '{self.drug2.id}'"
        return print_pddi_detected + "\n" + message
