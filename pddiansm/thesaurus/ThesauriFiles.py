import os
import importlib.resources as pkg_resources
from typing import List, Union

from pddiansm.thesaurus.ThesaurusExceptions import ThesaurusVersionNotFound
from pddiansm.thesaurus.ThesaurusFiles import ThesaurusFiles
from pddiansm.utils.Singleton import Singleton


class ThesauriFiles(metaclass=Singleton):
    def __init__(self):
        self.thesauri_files: List[ThesaurusFiles] = self.__load_thesauri_files()

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

    @classmethod
    def __load_thesauri_files(cls) -> List[ThesaurusFiles]:
        package_path = pkg_resources.path("pddiansm", "data")
        with package_path as path:
            thesauri_files: List[ThesaurusFiles] = []
            for root, subdirs, files in os.walk(path):
                json_files = list(filter(cls._is_a_json_file, files))
                cls.__create_and_add_thesaurus_files(root, json_files, thesauri_files)
            thesauri_files = sorted(thesauri_files, key=lambda thesaurus_file: thesaurus_file.thesaurus_version)
            return thesauri_files

    @classmethod
    def __create_and_add_thesaurus_files(cls, root: str, json_files: List[str],
                                         thesauri_files: List[ThesaurusFiles]) -> None:
        if len(json_files) == 0:
            return
        thesaurus_files = ThesaurusFiles(root)
        [thesaurus_files.add_json_file(json_file) for json_file in json_files]
        thesaurus_files.check_files()
        thesauri_files.append(thesaurus_files)

    @classmethod
    def _is_a_json_file(cls, file: str):
        return file.endswith(".json")
