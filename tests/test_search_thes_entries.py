import unittest
from typing import List

from pddiansm.thesaurus.IThesaurusEntriesFound import IThesaurusEntriesFound
from tests.test_detection import get_thesaurus_2009

from pddiansm.thesaurus.SearchThesEntries import SearchThesEntries

from pddiansm.thesaurus.ISearchThesEntries import ISearchThesEntries

from pddiansm.thesaurus.IThesaurus import IThesaurus


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        thesaurus: IThesaurus = get_thesaurus_2009()
        self.search_thes_entries: ISearchThesEntries = SearchThesEntries(thesaurus)

    def test_find_entries_substance_not_in_index(self):
        substance_not_in_index = "theine"
        thesaurus_entries: IThesaurusEntriesFound = self.search_thes_entries.search_moc(substance_not_in_index)
        substance_and_classes: List[str] = thesaurus_entries.get_list_of_substance_and_classes()
        self.assertTrue(substance_not_in_index in substance_and_classes)


if __name__ == '__main__':
    unittest.main()
