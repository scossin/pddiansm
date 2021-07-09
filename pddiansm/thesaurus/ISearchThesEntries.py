from typing import List

from pddiansm.mapper.DefaultMapper import DefaultMapper
from pddiansm.mapper.IMapper import IMapper
from pddiansm.thesaurus.IThesaurusEntriesFound import IThesaurusEntriesFound
from pddiansm.thesaurus.ThesaurusEntriesCollapsed import ThesaurusEntriesCollapsed


class ISearchThesEntries:
    """
    This class searches thesaurus entries (substances or drug classes") before searching PDDI
    """

    def __init__(self):
        self.mapper = DefaultMapper()

    def search_moc(self, moc: str) -> IThesaurusEntriesFound:
        """
        :param moc: a molecule or drug_class
        :return: thesaurus entries containing a list of substances and drug classes to search for PDDIs
        """
        pass

    def search_string(self, string: str) -> IThesaurusEntriesFound:
        """
        :param string: any string that could be map to substance(s) or drug_class(es) with a IMapper
        :return: thesaurus entries containing a list of substances and drug classes to search for PDDIs
        """
        mocs: List[str] = self.mapper.get_mocs_mapped(string)
        return self.search_mocs(mocs, string)

    def set_mapper(self, mapper: IMapper):
        self.mapper = mapper

    def search_mocs(self, mocs: List[str], string: str) -> IThesaurusEntriesFound:
        muliple_thesaurus_entries: List[IThesaurusEntriesFound] = [self.search_moc(moc) for moc in mocs]
        thesaurus_entries_collapsed: ThesaurusEntriesCollapsed = ThesaurusEntriesCollapsed(string,
                                                                                           muliple_thesaurus_entries)
        return thesaurus_entries_collapsed
