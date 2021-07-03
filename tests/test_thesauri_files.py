import unittest

from pddiansm.thesaurus.ThesauriFiles import ThesauriFiles
from pddiansm.thesaurus.Thesaurus import Thesaurus
from pddiansm.thesaurus.ThesaurusExceptions import ThesaurusVersionNotFound


class MyTestCase(unittest.TestCase):
    def test_thesauri_files(self):
        thesauri_files = ThesauriFiles()
        self.assertEqual(len(thesauri_files.get_thesauri_files()), 1)

    def test_list_versions(self):
        thesauri_files = ThesauriFiles()
        thesaurus_versions = thesauri_files.get_available_thesaurus_version()
        first_version = thesaurus_versions[0]
        self.assertEqual(first_version, "2019_09")

    def test_version_not_found(self):
        thesauri_files = ThesauriFiles()
        thesaurus_version = "2016_05"
        self.assertRaises(ThesaurusVersionNotFound, thesauri_files.get_thesaurus_files, thesaurus_version)

    def test_found_version(self):
        thesauri_files = ThesauriFiles()
        thesaurus_versions = thesauri_files.get_available_thesaurus_version()
        first_version = thesaurus_versions[0]
        thesaurus_files = thesauri_files.get_thesaurus_files(first_version)
        thesaurus = Thesaurus(thesaurus_files)
        self.assertIsInstance(thesaurus.pddis, list)
        self.assertEqual(len(thesaurus.pddis), 3035)


if __name__ == '__main__':
    unittest.main()