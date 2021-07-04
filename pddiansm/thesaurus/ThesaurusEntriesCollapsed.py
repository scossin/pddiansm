from typing import List

from pddiansm.thesaurus.IThesaurusEntries import IThesaurusEntries


class ThesaurusEntriesCollapsed(IThesaurusEntries):
    def __init__(self):
        self.mocs: List[str] = []

    def add_moc(self, moc):
        self.mocs.append(moc)

    def get_list_of_substance_and_classes(self) -> List[str]:
        return list(set(self.mocs))
