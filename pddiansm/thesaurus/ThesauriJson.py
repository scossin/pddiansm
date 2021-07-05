from typing import List

from pddiansm.thesaurus.IThesauri import IThesauri
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.ThesauriFiles import ThesauriFiles
from pddiansm.thesaurus.ThesaurusJson import ThesaurusJson
from pddiansm.utils.Singleton import Singleton


class ThesauriJson(IThesauri, metaclass=Singleton):
    def __init__(self):
        self.instances: {str: List[IThesaurus]} = {}
        self.thesauri_files: ThesauriFiles = ThesauriFiles()

    def get_thesaurus(self, thesaurus_version) -> IThesaurus:
        """ Overrides """
        thesaurus_files = self.thesauri_files.get_thesaurus_files(thesaurus_version)
        if self.__thesaurus_is_not_loaded(thesaurus_version):
            self.__load_thesaurus(thesaurus_files)
        return self.instances[thesaurus_version]

    def get_available_thesaurus_version(self) -> List[str]:
        """ Overrides """
        return self.thesauri_files.get_available_thesaurus_version()

    def __thesaurus_is_not_loaded(self, thesaurus_version):
        return thesaurus_version not in self.instances

    def __load_thesaurus(self, thesaurus_files) -> None:
        thesaurus = ThesaurusJson(thesaurus_files)
        self.instances[thesaurus_files.thesaurus_version] = thesaurus
