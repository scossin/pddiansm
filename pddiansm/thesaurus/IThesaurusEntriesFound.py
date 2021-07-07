from typing import List


class IThesaurusEntriesFound:

    def __init__(self, searched_string: str):
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
