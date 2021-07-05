from typing import List, TextIO, Dict

from pddiansm.mapper.IMapper import IMapper
from pddiansm.utils.normalize_string import normalize_string


class MappingFile(IMapper):
    """
    Load a mapping file containing 2 columns, in this order:
        1) the name of a molecule or drug_class listed in the thesaurus
        2) an identifier
    An identifier can match one to several substance(s) and drug_class(es).
    """
    def __init__(self, filename: str, sep="\t", header=True):
        self.filename: str = filename
        self.map_identifier_2_mocs: Dict[str, List[str]] = {}
        with open(filename, "r") as f:
            self.__remove_first_line_if_header(f, header)
            for line in f:
                self.__fill_map_identifier_2_moc(line, sep)

    def get_mocs_mapped(self, identifier: str) -> List[str]:
        """ Overrides """
        return self.map_identifier_2_mocs.get(identifier, IMapper.DEFAULT_IF_IDENTIFIER_NOT_MAPPED)

    def __fill_map_identifier_2_moc(self, line: str, sep: str) -> None:
        columns: List[str] = line.split(sep)
        self.__check_2_columns(line, columns)
        substance, identifier = columns  # Destructuring, substance must be in first column
        identifier = identifier.strip()
        normalized_substance = normalize_string(substance)
        self.__create_empty_list_if_identifier_not_exists(identifier)
        self.__append_if_not_exists(identifier, normalized_substance)

    @staticmethod
    def __remove_first_line_if_header(f: TextIO, header: bool) -> None:
        if header:
            next(f)

    def __create_empty_list_if_identifier_not_exists(self, identifier: str) -> None:
        if identifier not in self.map_identifier_2_mocs:
            self.map_identifier_2_mocs[identifier] = []

    def __check_2_columns(self, line, columns) -> None:
        if len(columns) != 2:
            raise TypeError(f"expected 2 columns in {self.filename} but got {len(columns)} at line {line}")

    def __append_if_not_exists(self, identifier, normalized_substance) -> None:
        if normalized_substance not in self.map_identifier_2_mocs[identifier]:
            self.map_identifier_2_mocs[identifier].append(normalized_substance)
