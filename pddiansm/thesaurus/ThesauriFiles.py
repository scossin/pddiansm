import os
import importlib.resources as pkg_resources
from typing import List

from pddiansm.thesaurus.ThesaurusExceptions import ThesaurusVersionNotFound
from pddiansm.thesaurus.ThesaurusFiles import ThesaurusFiles


class ThesauriFiles:
    def __init__(self):
        self.thesauri_files: List[ThesaurusFiles] = self.load_thesauri_files()

    def get_thesauri_files(self) -> List[ThesaurusFiles]:
        return self.thesauri_files

    def get_thesaurus_files(self, thesaurus_version: str):
        thesaurus_files_list = [thesaurus_files for thesaurus_files in self.thesauri_files
                                if thesaurus_files.thesaurus_version == thesaurus_version]
        if len(thesaurus_files_list) == 0:
            raise ThesaurusVersionNotFound(f"{thesaurus_version} was not found")
        return thesaurus_files_list[0]

    def get_available_thesaurus_version(self) -> List[str]:
        versions = [thesaurus_files.thesaurus_version for thesaurus_files in self.thesauri_files]
        return sorted(versions)

    def print_available_thesaurus_version(self) -> None:
        [print(version) for version in self.get_available_thesaurus_version()]

    @classmethod
    def load_thesauri_files(cls) -> List[ThesaurusFiles]:
        package_path = pkg_resources.path("pddiansm", "data")
        with package_path as path:
            thesauri_files = []
            for root, subdirs, files in os.walk(path):
                json_files = list(filter(cls._is_a_json_file, files))
                new_thesaurus_files = cls.__create_thesaurus_files(root, json_files)
                thesauri_files.append(new_thesaurus_files)
            thesauri_files: List[ThesaurusFiles] = [thesaurus_files for thesaurus_files in thesauri_files
                                                    if thesaurus_files is not None]
            [thesaurus_files.check_files() for thesaurus_files in thesauri_files]
            thesauri_files = sorted(thesauri_files, key=lambda thesaurus_file: thesaurus_file.thesaurus_version)
            return thesauri_files

    @classmethod
    def __create_thesaurus_files(cls, root, json_files) -> ThesaurusFiles:
        if len(json_files) == 0:
            return None
        thesaurus_file = ThesaurusFiles(root)
        [thesaurus_file.add_json_file(json_file) for json_file in json_files]
        return thesaurus_file

    @classmethod
    def _is_a_json_file(cls, file: str):
        return file.endswith(".json")
