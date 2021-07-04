from typing import List

from pddiansm.detector.PDDIdetected import PDDIdetected
from pddiansm.detector.PDDIdetector import PDDIdetector
from pddiansm.interfaces.interfaces_pddi import PDDI
from pddiansm.mapper.IMapper import IMapper
from pddiansm.mapper.StringMapper import StringMapper
from pddiansm.thesaurus.Thesaurus import Thesaurus
from pddiansm.thesaurus.ThesaurusEntries import ThesaurusEntries


class PDDIansmDetector(PDDIdetector):
    def __init__(self, thesaurus: Thesaurus):
        """
        Detect potential drug drug interactions (PDDI) between two substance or drug_class
        :param version: a ANSM thesaurus version
        """
        self.thesaurus = thesaurus
        self.mapper: IMapper = StringMapper(thesaurus)
        self.indexed_entries = {}  # thesaurus molecules and classes are indexed for fast look-up
        self.__create_indexed_entries(thesaurus.pddis)

    def detect_pddi(self, molecule_or_class1: str, molecule_or_class2: str) -> List[PDDIdetected]:
        """
        Detect all potential drug drug interactions in the ANSM guidelines document
        from two molecules or classes in string format
        :param molecule_or_class1: a molecule or a drug class (string)
        :param molecule_or_class2: a molecule or a drug class (string)
        :return: a List of PDDIsubstance containing the PDDI
        """
        thesaurus_entries_1: ThesaurusEntries = self.mapper.search_moc(molecule_or_class1)
        thesaurus_entries_2: ThesaurusEntries = self.mapper.search_moc(molecule_or_class2)
        pddis: List[PDDI] = self.search_pddi_thesaurus(thesaurus_entries_1, thesaurus_entries_2)
        pddi_detected: List[PDDIdetected] = [PDDIdetected(pddi, molecule_or_class1, molecule_or_class2)
                                             for pddi in pddis]
        return pddi_detected

    def search_pddi_thesaurus(self, thesaurus_entries_1: ThesaurusEntries,
                              thesaurus_entries_2: ThesaurusEntries) -> List[PDDI]:
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
