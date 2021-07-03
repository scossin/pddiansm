from typing import List, Union

from pddiansm.detector.PDDIdetector import PDDIdetector
from pddiansm.interfaces.interfaces_pddi import PDDI, SubstanceThesaurus, ClassThesaurus
from pddiansm.thesaurus.Thesaurus import Thesaurus


class PDDIansmDetector(PDDIdetector):
    def __init__(self, thesaurus: Thesaurus):
        """
        Detect potential drug drug interactions (PDDI) between two substance or drug_class
        :param version: a ANSM thesaurus version
        """
        self.thesaurus = thesaurus
        self.indexed_entries = {}  # thesaurus molecules and classes are indexed for fast look-up
        self.__create_indexed_entries(thesaurus.pddis)

    def detect_pddi(self, molecule_or_class1: str, molecule_or_class2: str) -> List[PDDI]:
        """
        Detect all potential drug drug interactions in the ANSM guidelines document
        from two molecules or classes in string format
        :param molecule_or_class1: a molecule or a drug class (string)
        :param molecule_or_class2: a molecule or a drug class (string)
        :return: a List of PDDIsubstance containing the PDDI
        """
        # moc: molecule_or_class
        # if moc is a molecule, we retrieve all its drug_classes first and we search PDDIs
        # if moc is a drug_class, we don't retrieve all the molecule it contains because each molecule may interact on their own
        moc_thesaurus1 = self.thesaurus.search_molecule_or_class(molecule_or_class1)
        moc_thesaurus2 = self.thesaurus.search_molecule_or_class(molecule_or_class2)
        pddis = self.detect_pddi_thesaurus(moc_thesaurus1, moc_thesaurus2)
        return pddis

    def detect_pddi_thesaurus(self, moc1: Union[SubstanceThesaurus, ClassThesaurus],
                              moc2: Union[SubstanceThesaurus, ClassThesaurus]) -> List[PDDI]:
        """
        Detect all potential drug drug interactions in the ANSM guidelines document
        from two SubstanceThesaurus or ClassThesaurus
        :param moc1: a `SubstanceThesaurus` or `ClassThesaurus` representing substance / classe in the ANSM reference document
        :param moc2: a `SubstanceThesaurus` or `ClassThesaurus` representing substance / classe in the ANSM reference document
        :return: a List of PDDIsubstance containing the PDDI
        """
        if moc1 is None or moc2 is None:
            return []
        mol_and_classes1 = self.__get_list_of_substance_and_classes(moc1)
        mol_and_classes2 = self.__get_list_of_substance_and_classes(moc2)
        pddis: List[PDDI] = [self._search_pddi_in_index(molecule_or_class1, molecule_or_class2)
                             for molecule_or_class1 in mol_and_classes1
                             for molecule_or_class2 in mol_and_classes2]
        pddis: List[PDDI] = self.__remove_none_values(pddis)
        return pddis

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

    def _search_pddi_in_index(self, molecule_or_class1: str, molecule_or_class2: str) -> PDDI:
        moc1_interact_with = self.indexed_entries.get(molecule_or_class1, {})
        pddi = moc1_interact_with.get(molecule_or_class2, None)
        return pddi

    @staticmethod
    def __get_list_of_substance_and_classes(moc: Union[SubstanceThesaurus, ClassThesaurus]) -> List[str]:
        if isinstance(moc, SubstanceThesaurus):
            list_of_substance_and_classes = moc.drug_classes[:]
            list_of_substance_and_classes.append(moc.substance)
        elif isinstance(moc, ClassThesaurus):
            # below we ignore substances of the class (moc.substances is not added) because
            # each substance can interact on their own and we want to be sure the interaction is at the class level.
            list_of_substance_and_classes = [moc.drug_class]
        else:
            raise TypeError(f"moc argument is not of type SubstanceThesaurus or ClassThesaurus")
        return list_of_substance_and_classes

