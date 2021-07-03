from pddiansm.interfaces.interfaces_input import SimpleDrug
from pddiansm.interfaces.interfaces_pddi import PDDI


class PDDIdrugsDetected:
    def __init__(self, pddi: PDDI, drug1: SimpleDrug, drug2: SimpleDrug, i_1: int, i_2: int):
        """
        A pddi detected between one substance of drug1 and another substance of drug2
        :param pddi: a potential drug drug interaction
        :param drug1: the first drug that interacts
        :param drug2: the second drug that interacts
        :param i_1: the ith substance of drug1 that interacts the ith substance of drug2
        :param i_2: the ith substance of drug2
        """
        self.pddi = pddi
        self.drug1 = drug1
        self.drug2 = drug2
        self.i_1 = i_1
        self.i_2 = i_2

    def get_dict_representation(self):
        return {
            "drug_id_1": self.drug1.id,
            "substance1": self.drug1.substances[self.i_1].substance,
            "ith_substance_1": self.i_1,
            "drug_id_2": self.drug2.id,
            "substance2": self.drug2.substances[self.i_2].substance,
            "ith_substance_2": self.i_2,
            "pddi": self.__get_dict_representation_pddi()
        }

    def __get_dict_representation_pddi(self):
        pddi = self.pddi
        severity_levels = [{"level": severity_info.level,
                            "info": severity_info.info}
                           for severity_info in pddi.severity_levels]
        return {
            "pddi_id": self.__get_pddi_id(),
            "main_drug": pddi.main_drug,
            "between_main_and_plus_drug": pddi.between_main_and_plus_drug,
            "plus_drug": pddi.plus_drug,
            "severity_levels": severity_levels,
            "interaction_mechanism": pddi.interaction_mechanism,
            "description": pddi.description
        }

    def __get_pddi_id(self):
        return self.pddi.main_drug + ";" + self.pddi.plus_drug

    def __str__(self):
        substance1 = self.drug1.substances[self.i_1].substance
        substance2 = self.drug2.substances[self.i_2].substance
        return f"{substance1} ({self.pddi.main_drug}) can interact with {substance2} ({self.pddi.plus_drug})"
