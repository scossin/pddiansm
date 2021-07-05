from typing import List

from pddiansm.mapper.DefaultMapper import DefaultMapper
from pddiansm.mapper.IMapper import IMapper
from pddiansm.thesaurus.IThesaurusEntries import IThesaurusEntries
from pddiansm.thesaurus.ThesaurusEntriesCollapsed import ThesaurusEntriesCollapsed


class ISearchThesEntries:

    def __init__(self):
        self.mapper = DefaultMapper()

    def search_moc(self, moc: str) -> IThesaurusEntries:
        """
        :param moc: a molecule or drug_class
        :return: thesaurus entries containing a list of substances and drug classes to search for PDDIs
        """
        pass

    def search_string(self, string: str) -> IThesaurusEntries:
        """
        :param string: any string that could be map to substance(s) or drug_class(es) with a IMapper
        :return: thesaurus entries containing a list of substances and drug classes to search for PDDIs
        """
        mocs: List[str] = self.mapper.get_mocs_mapped(string)
        return self.search_mocs(mocs)

    def set_mapper(self, mapper: IMapper):
        self.mapper = mapper

    def search_mocs(self, mocs: List[str]) -> IThesaurusEntries:
        muliple_thesaurus_entries: List[IThesaurusEntries] = [self.search_moc(moc) for moc in mocs]
        thesaurus_entries_collapsed: IThesaurusEntries = ThesaurusEntriesCollapsed()
        for thesaurus_entries in muliple_thesaurus_entries:
            for moc in thesaurus_entries.get_list_of_substance_and_classes():
                thesaurus_entries_collapsed.add_moc(moc)
        return thesaurus_entries_collapsed
