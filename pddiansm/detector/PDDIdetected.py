from pddiansm.interfaces.interfaces_output import PDDIdetected
from pddiansm.interfaces.interfaces_pddi import PDDI


class PDDIdetected:
    def __init__(self, pddi: PDDI, molecule_or_class1: str, molecule_or_class2: str):
        self.pddi = pddi
        self.moc1 = molecule_or_class1
        self.moc2 = molecule_or_class2

    @property
    def main_drug(self):
        return self.pddi.main_drug

    @property
    def between_main_and_plus_drug(self):
        return self.pddi.between_main_and_plus_drug

    @property
    def plus_drug(self):
        return self.pddi.plus_drug

    @property
    def severity_levels(self):
        return self.pddi.severity_levels

    @property
    def interaction_mechanism(self):
        return self.pddi.interaction_mechanism

    @property
    def description(self):
        return self.pddi.description

    @classmethod
    def get_pddi_id(cls, pddi: PDDI):
        main_entries = [pddi.main_drug, pddi.plus_drug]
        main_entries = sorted(main_entries)
        return ";".join(main_entries)

    def __str__(self):
        return f"{self.moc1} (from  '{self.pddi.main_drug}') can interact with {self.moc2} (from '{self.pddi.plus_drug}')"


def build_pddi_detected(pddi, molecule_or_class1, molecule_or_class2) -> PDDIdetected:
    if pddi is None:
        return None
    return PDDIdetected(pddi, molecule_or_class1, molecule_or_class2)
