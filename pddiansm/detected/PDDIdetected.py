from typing import Dict

from pddiansm.pydantic.interfaces_pddi import PDDI
from pddiansm.thesaurus import IThesaurusEntriesFound
from pddiansm.thesaurus.IThesaurus import IThesaurus


class PDDIdetected:
    def __init__(self, pddi: PDDI, thesaurus_entries_1: IThesaurusEntriesFound,
                 thesaurus_entries_2: IThesaurusEntriesFound, thesaurus: IThesaurus):
        self.pddi = pddi
        self.moc1 = thesaurus_entries_1.get_searched_string()
        self.moc2 = thesaurus_entries_2.get_searched_string()
        self.thesaurus: IThesaurus = thesaurus
        self.id = get_pddi_detected_id(self)
        self.mocs_belong_to_plus_and_main_drugs = self.__are_mocs_belonging_to_both_entries(thesaurus_entries_1,
                                                                                            thesaurus_entries_2)
        # Why we need "mocs_belong_to_both_entries" is a bit tricky
        # When we search a PDDI between 2 molecules (mol1, mol2), the order doesn't matter
        # which means pddi(mol1, mol2) equals pddi(mol2, mol1) ; to remove duplicate we can use set()
        # But in some cases mol1 and mol2 belong to 2 drug_classes that interact so mol1 and mol2 can be swapped
        # (without changing main and plus_drug)
        # Ex: "domperidone (from 'substances susceptibles de donner des torsades de pointes') can interact
        # with escitalopram (from 'torsadogenes (sauf arsenieux, antiparasitaires, neuroleptiques, methadone...)')
        # Also True is to say:
        # Ex: "escitalopram (from 'substances susceptibles de donner des torsades de pointes') can interact
        # with domperidone (from 'torsadogenes (sauf arsenieux, antiparasitaires, neuroleptiques, methadone...)')
        # because escitalopram and domperidone belong to both drug_classes
        # Although these 2 PDDI are the same, it's important to mention this information:
        # Ex: "domperidone(or escitalopram) (from 'substances susceptibles de donner des torsades de pointes') can interact
        # with escitalopram(or domperidone) (from 'torsadogenes (sauf arsenieux, antiparasitaires, neuroleptiques, methadone...)')

    def __str__(self):
        return f"{self.__get_moc_from_main_drug()} (from '{self.pddi.main_drug}') " \
               f"can interact with {self.__get_moc_from_plus_drug()} (from '{self.pddi.plus_drug}')" \
               f" in thesaurus version {self.thesaurus.get_thesaurus_version()}"

    def __eq__(self, other):
        """
        Two pddi_detected are the same if:
            - the pddi_id is the same
            - moc1 and moc2 are the same whatever their order
        """
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def as_dict(self) -> Dict:
        """Get a dictionary representation of the PDDI detected between 2 molecules or classes searched"
        :return: dictionary containing information on the PDDI and the searched strings
        :rtype: a dictionary
        """
        severity_levels = [{"level": severity_info.level,
                            "info": severity_info.info}
                           for severity_info in self.severity_levels]
        return {
            "pddi_id": get_pddi_id(self.thesaurus.get_thesaurus_version(), self.pddi),
            "pddi_detected_id": get_pddi_detected_id(self),
            "main_drug": self.main_drug,
            "moc1": self.moc1,
            "between_main_and_plus_drug": self.between_main_and_plus_drug,
            "plus_drug": self.plus_drug,
            "moc2": self.moc2,
            "moc1_moc2_can_be_swapped": self.mocs_belong_to_plus_and_main_drugs,
            "severity_levels": severity_levels,
            "interaction_mechanism": self.interaction_mechanism,
            "description": self.description,
        }

    def __get_moc_from_main_drug(self) -> str:
        if self.mocs_belong_to_plus_and_main_drugs:
            return self.__get_moc1_and_moc2(self.moc1, self.moc2)
        else:
            return self.moc1

    def __get_moc_from_plus_drug(self) -> str:
        if self.mocs_belong_to_plus_and_main_drugs:
            return self.__get_moc1_and_moc2(self.moc2, self.moc1)
        else:
            return self.moc2

    @staticmethod
    def __get_moc1_and_moc2(moc1: str, moc2: str) -> str:
        moc1_and_moc2 = f"{moc1}(or {moc2})"
        return moc1_and_moc2

    def __are_mocs_belonging_to_both_entries(self, thesaurus_entries1, thesaurus_entries2) -> bool:
        if self.__mols_are_the_same():
            return True
        if self.mol1_belongs_to_plus_drug(thesaurus_entries2) and self.mol2_belongs_to_main_drug(thesaurus_entries1):
            return True
        return False

    def __mols_are_the_same(self) -> bool:
        return self.moc1 == self.moc2

    def mol1_belongs_to_plus_drug(self, thesaurus_entries1: IThesaurusEntriesFound) -> bool:
        return self.plus_drug in thesaurus_entries1.get_drug_classes()

    def mol2_belongs_to_main_drug(self, thesaurus_entries2: IThesaurusEntriesFound) -> bool:
        return self.main_drug in thesaurus_entries2.get_drug_classes()

    @property
    def main_drug(self):
        return self.pddi.main_drug

    @property
    def between_main_and_plus_drug(self):
        return self.pddi.between_main_and_plus_drug

    @property
    def plus_drug(self):
        return self.pddi.plus_drug

    @property
    def severity_levels(self):
        return self.pddi.severity_levels

    @property
    def interaction_mechanism(self):
        return self.pddi.interaction_mechanism

    @property
    def description(self):
        return self.pddi.description


def get_pddi_id(thesaurus_version: str, pddi: PDDI) -> str:
    """
    The id is used to remove PDDI duplicates
    the id is created by concatenating: thesaurus_version;entry1;entry2
    where entry1 and entry2 are main_drug or plus_drug (sorted alphabetically)
    :param thesaurus_version:
    :param pddi:
    :return: an id for this pddi
    :rtype: a string
    """
    main_entries = [pddi.main_drug, pddi.plus_drug]
    main_entries = sorted(main_entries)
    main_entries_id = ";".join(main_entries)
    pddi_id = thesaurus_version + ";" + main_entries_id
    return pddi_id


def get_pddi_detected_id(pddi_detected: PDDIdetected) -> str:
    """
    The id is used to remove PDDI duplicates
    the id is created by concatenating: pddi_id;moc1;moc2
    where moc1 and moc2 are molecule or classe (moc) sorted alphabetically
    :param pddi_detected:
    :return: an id for this pddi_detected
    :rtype:
    """
    thesaurus_version = pddi_detected.thesaurus.get_thesaurus_version()
    pddi_id = get_pddi_id(thesaurus_version, pddi_detected.pddi)
    mocs = [pddi_detected.moc1, pddi_detected.moc2]
    mocs = sorted(mocs)
    mocs_id = ";".join(mocs)
    pddi_detected_id = pddi_id + mocs_id
    return pddi_detected_id
