from typing import List


class IThesaurusEntriesFound:
    """
    The steps to find PDDIs are:
    1) A string in input that can be mapped to substances and drug classes
    2) Map this string to a list of string, can be substances or drug classes, with a IMapper
    3) Match thesaurus entries with IThesaurusEntriesFound (retrieve drug classes of a substance here)
    4) Search PDDIs with IThesaurusEntriesFound
    """

    def __init__(self, searched_string: str):
        """
        :param searched_string: the string (molecule, drug class or identifier) that was searched
        """
        self.searched_string = searched_string

    def get_searched_string(self) -> str:
        return self.searched_string

    def get_substances(self) -> List[str]:
        pass

    def get_drug_classes(self) -> List[str]:
        pass

    def get_list_of_substance_and_classes(self) -> List[str]:
        """ Overrides """
        substance_and_classes = list(set(self.substances)) + list(set(self.drug_classes))  # to be sure everything is unique
        return substance_and_classes
