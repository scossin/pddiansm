from typing import List

from pddiansm.mapper.IMapper import IMapper
from pddiansm.mapper.ISubstanceMapping import ISubstanceMapping
from pddiansm.mapper.StringMapper import StringMapper
from pddiansm.thesaurus.IThesaurusEntries import IThesaurusEntries
from pddiansm.thesaurus.ThesaurusEntriesCollapsed import ThesaurusEntriesCollapsed


class IdentifierMapper(IMapper):
    def __init__(self, string_mapper: StringMapper, substance_mapping: ISubstanceMapping):
        self.string_mapper = string_mapper
        self.substance_mapping = substance_mapping

    def search_moc(self, string: str) -> IThesaurusEntries:
        """ Overrides """
        return self.search_moc_by_identifier(string)

    def search_moc_by_identifier(self, identifier) -> IThesaurusEntries:
        mocs = self.substance_mapping.get_substances_mapped(identifier)
        muliple_thesaurus_entries: List[IThesaurusEntries] = [self.string_mapper.search_moc(moc) for moc in mocs]
        thesaurus_entries_collapsed = self.__collapse_thesaurus_entries(muliple_thesaurus_entries)
        return thesaurus_entries_collapsed

    @staticmethod
    def __collapse_thesaurus_entries(muliple_thesaurus_entries: List[IThesaurusEntries]) -> IThesaurusEntries:
        thesaurus_entries_collapsed: IThesaurusEntries = ThesaurusEntriesCollapsed()
        for thesaurus_entries in muliple_thesaurus_entries:
            for moc in thesaurus_entries.get_list_of_substance_and_classes():
                thesaurus_entries_collapsed.add_moc(moc)
        return thesaurus_entries_collapsed
