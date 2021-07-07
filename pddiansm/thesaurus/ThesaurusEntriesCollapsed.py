from typing import List

from pddiansm.thesaurus.IThesaurusEntriesFound import IThesaurusEntriesFound
from pddiansm.thesaurus.ThesaurusEntriesImp import ThesaurusEntriesImp


class ThesaurusEntriesCollapsed(ThesaurusEntriesImp):
    def __init__(self, searched_string: str, thesaurus_entries: List[IThesaurusEntriesFound]):
        super().__init__(searched_string)
        self.__collapsed_found_thesaurus_entries(thesaurus_entries)

    def __collapsed_found_thesaurus_entries(self, thesaurus_entries: List[IThesaurusEntriesFound]):
        for thesaurus_entry in thesaurus_entries:
            [self.add_substance(substance) for substance in thesaurus_entry.get_substances()]
            [self.add_drug_class(drug_class) for drug_class in thesaurus_entry.get_drug_classes()]
