from typing import Dict

from pddiansm.interfaces.interfaces_pddi import SubstanceThesaurus, ClassThesaurus
from pddiansm.mapper.IMapper import IMapper
from pddiansm.thesaurus.Thesaurus import Thesaurus
from pddiansm.thesaurus.ThesaurusEntries import ThesaurusEntries
from pddiansm.utils.normalize_string import normalize_string


class StringMapper(IMapper):

    def __init__(self, thesaurus: Thesaurus):
        self.thesaurus = thesaurus
        self.hashmap_substances: Dict[str, SubstanceThesaurus] = self.__create_hashmap_substances()
        self.hashmap_drug_classes: Dict[str, ClassThesaurus] = self.__create_hashmap_drug_classes()

    def search_moc(self, string: str) -> ThesaurusEntries:
        """ Overrides :func:`IMapper.search_moc()`"""
        return self.search_moc_by_string(string)

    def search_moc_by_string(self, moc: str) -> ThesaurusEntries:
        """
        Find substances and drug_classes matching this moc by string matching
        :param moc: a molecule or a drug_class
        """
        thesaurus_entries = ThesaurusEntries(moc)
        normalized_moc = normalize_string(moc)
        self.__add_substance_and_drug_classes_if_moc_is_a_substance(thesaurus_entries, normalized_moc)
        self.__add_drug_classes_if_moc_is_a_drug_class(thesaurus_entries, normalized_moc)
        return thesaurus_entries

    def __add_substance_and_drug_classes_if_moc_is_a_substance(self, thesaurus_entries: ThesaurusEntries,
                                                               normalized_moc: str) -> None:
        if normalized_moc in self.hashmap_substances:
            substance_thesaurus = self.hashmap_substances[normalized_moc]
            thesaurus_entries.add_substance(substance_thesaurus.substance)
            [thesaurus_entries.add_drug_class(drug_class) for drug_class in substance_thesaurus.drug_classes]

    def __add_drug_classes_if_moc_is_a_drug_class(self, thes_entries: ThesaurusEntries, normalized_moc: str) -> None:
        if normalized_moc in self.hashmap_drug_classes:
            drug_class_thesaurs = self.hashmap_drug_classes[normalized_moc]
            thes_entries.add_drug_class(drug_class_thesaurs.drug_class)
            [thes_entries.add_drug_class(drug_class) for drug_class in drug_class_thesaurs.parent_drug_classes]

    def __create_hashmap_substances(self) -> Dict[str, SubstanceThesaurus]:
        hashmap_substances = {substance_thesaurus.substance: substance_thesaurus
                              for substance_thesaurus in self.thesaurus.substances_thesaurus}
        return hashmap_substances

    def __create_hashmap_drug_classes(self) -> Dict[str, ClassThesaurus]:
        drug_classes = self.thesaurus.get_unique_drug_classes()
        # TODO: find parent_drug_classes of a drug_class
        hashmap_drug_classes = {drug_class: ClassThesaurus(drug_class=drug_class, parent_drug_classes=[])
                                for drug_class in drug_classes}
        return hashmap_drug_classes
