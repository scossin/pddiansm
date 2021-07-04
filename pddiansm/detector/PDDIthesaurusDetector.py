from typing import List

from pddiansm.detector.PDDIdetected import PDDIdetected
from pddiansm.detector.IPDDIdetector import IPDDIdetector
from pddiansm.pydantic.interfaces_pddi import PDDI
from pddiansm.mapper.IMapper import IMapper
from pddiansm.mapper.StringMapper import StringMapper
from pddiansm.thesaurus.IThesaurusEntries import IThesaurusEntries
from pddiansm.thesaurus.ThesaurusJson import IThesaurus


class PDDIthesaurusDetector(IPDDIdetector):
    def __init__(self, thesaurus: IThesaurus):
        """
        Detect potential drug drug interactions (PDDI) between two substance or drug_class
        :param version: a ANSM thesaurus version
        """
        self.thesaurus: IThesaurus = thesaurus
        self.string_mapper: StringMapper = StringMapper(thesaurus)
        self.mapper: IMapper = self.string_mapper  # default mapper
        self.indexed_entries = {}  # thesaurus molecules and classes are indexed for fast look-up
        self.__create_indexed_entries(thesaurus.get_pddis())

    def detect_pddi(self, string1: str, string2: str) -> List[PDDIdetected]:
        """ Overrides """
        thesaurus_entries_1: IThesaurusEntries = self.mapper.search_moc(string1)
        thesaurus_entries_2: IThesaurusEntries = self.mapper.search_moc(string2)
        pddis: List[PDDI] = self._search_pddi_thesaurus(thesaurus_entries_1, thesaurus_entries_2)
        pddis_detected: List[PDDIdetected] = [
            PDDIdetected(pddi, string1, string2, self.thesaurus.get_thesaurus_version())
            for pddi in pddis]
        pddis_detected = self._remove_duplicates(pddis_detected)
        return pddis_detected

    def set_mapper(self, mapper: IMapper) -> None:
        self.mapper = mapper

    def _search_pddi_thesaurus(self, thesaurus_entries_1: IThesaurusEntries,
                               thesaurus_entries_2: IThesaurusEntries) -> List[PDDI]:
        """
        Detect all potential drug drug interactions in the ANSM guidelines document
        given several thesaurus entries (substances or drug_classes)
        """
        mol_and_classes1 = thesaurus_entries_1.get_list_of_substance_and_classes()
        mol_and_classes2 = thesaurus_entries_2.get_list_of_substance_and_classes()
        pddis: List[PDDI] = [self._search_pddi_in_index(molecule_or_class1, molecule_or_class2)
                             for molecule_or_class1 in mol_and_classes1
                             for molecule_or_class2 in mol_and_classes2]
        pddis: List[PDDI] = self.__remove_none_values(pddis)
        return pddis

    def _search_pddi_in_index(self, molecule_or_class1: str, molecule_or_class2: str) -> PDDI:
        moc1_interact_with = self.indexed_entries.get(molecule_or_class1, {})
        pddi = moc1_interact_with.get(molecule_or_class2, None)
        return pddi

    @staticmethod
    def _remove_duplicates(pddis_detected: List[PDDIdetected]) -> List[PDDIdetected]:
        """ Duplicates can happen if :
            1) moc1 and moc2 belong to the same drug_class and this drug_class interactfs with itself
            2) moc1 is the same as moc2 and 1) is true
        """
        return list(set(pddis_detected))

    @staticmethod
    def __remove_none_values(pddis):
        return [pddi for pddi in pddis if pddi is not None]

    def __create_indexed_entries(self, pddis):
        [self.__add_pddi(pddi) for pddi in pddis]

    def __add_pddi(self, pddi):
        self.__add_entry_in_index(pddi.main_drug, pddi.plus_drug, pddi)
        self.__add_entry_in_index(pddi.plus_drug, pddi.main_drug, pddi)

    def __add_entry_in_index(self, molecule_or_class1: str, molecule_or_class2: str, pddi: PDDI):
        if molecule_or_class1 not in self.indexed_entries:
            self.indexed_entries[molecule_or_class1] = {}
        dict_interact_with = self.indexed_entries[molecule_or_class1]
        dict_interact_with[molecule_or_class2] = pddi
