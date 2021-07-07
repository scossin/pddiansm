from typing import List

from pddiansm.thesaurus.IThesaurusEntriesFound import IThesaurusEntriesFound


class ThesaurusEntriesImp(IThesaurusEntriesFound):
    def __init__(self, searched_string):
        super().__init__(searched_string)
        self.substances = []
        self.drug_classes = []

    def add_substance(self, substance: str) -> None:
        self.substances.append(substance)

    def add_drug_class(self, drug_class: str) -> None:
        self.drug_classes.append(drug_class)

    def get_substances(self) -> List[str]:
        return self.substances

    def get_drug_classes(self) -> List[str]:
        return self.drug_classes
