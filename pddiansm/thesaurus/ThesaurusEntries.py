from typing import List


class ThesaurusEntries:
    def __init__(self, search_moc):
        self.substances = []
        self.drug_classes = []
        self.search_moc = search_moc

    def add_substance(self, substance: str):
        self.substances.append(substance)

    def add_drug_class(self, drug_class):
        self.drug_classes.append(drug_class)

    def get_list_of_substance_and_classes(self) -> List[str]:
        substance_and_classes = self.substances + self.drug_classes
        return substance_and_classes

