from typing import Dict

from pddiansm.pydantic.interfaces_pddi import SubstanceThesaurus, ClassThesaurus
from pddiansm.thesaurus.ISearchThesEntries import ISearchThesEntries
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.IThesaurusEntriesFound import IThesaurusEntriesFound
from pddiansm.thesaurus.ThesaurusEntriesImp import ThesaurusEntriesImp
from pddiansm.utils.normalize_string import normalize_string


class SearchThesEntries(ISearchThesEntries):

    def __init__(self, thesaurus: IThesaurus):
        super().__init__()
        self.thesaurus: IThesaurus = thesaurus
        self.hashmap_substances: Dict[str, SubstanceThesaurus] = self.__create_hashmap_substances()
        self.hashmap_drug_classes: Dict[str, ClassThesaurus] = self.__create_hashmap_drug_classes()

    def search_moc(self, moc: str) -> IThesaurusEntriesFound:
        """ Overrides
        Find substances and drug_classes matching this moc by string matching
        :param moc: a molecule or a drug_class
        """
        thesaurus_entries = ThesaurusEntriesImp(moc)
        normalized_moc = normalize_string(moc)
        self.__add_substance_and_drug_classes_if_moc_is_a_substance(thesaurus_entries, normalized_moc)
        self.__add_drug_classes_if_moc_is_a_drug_class(thesaurus_entries, normalized_moc)
        return thesaurus_entries

    def __add_substance_and_drug_classes_if_moc_is_a_substance(self, thesaurus_entries: ThesaurusEntriesImp,
                                                               normalized_moc: str) -> None:
        if normalized_moc in self.hashmap_substances:
            substance_thesaurus = self.hashmap_substances[normalized_moc]
            thesaurus_entries.add_substance(substance_thesaurus.substance)
            [thesaurus_entries.add_drug_class(drug_class) for drug_class in substance_thesaurus.drug_classes]

    def __add_drug_classes_if_moc_is_a_drug_class(self, thes_entries: ThesaurusEntriesImp, normalized_moc: str) -> None:
        if normalized_moc in self.hashmap_drug_classes:
            drug_class_thesaurs = self.hashmap_drug_classes[normalized_moc]
            thes_entries.add_drug_class(drug_class_thesaurs.drug_class)
            [thes_entries.add_drug_class(drug_class) for drug_class in drug_class_thesaurs.parent_drug_classes]

    def __create_hashmap_substances(self) -> Dict[str, SubstanceThesaurus]:
        hashmap_substances = {substance_thesaurus.substance: substance_thesaurus
                              for substance_thesaurus in self.thesaurus.get_substances_thesaurus()}
        return hashmap_substances

    def __create_hashmap_drug_classes(self) -> Dict[str, ClassThesaurus]:
        drug_classes = self.thesaurus.get_unique_drug_classes()
        # TODO: find parent_drug_classes of a drug_class
        hashmap_drug_classes = {drug_class: ClassThesaurus(drug_class=drug_class, parent_drug_classes=[])
                                for drug_class in drug_classes}
        return hashmap_drug_classes
