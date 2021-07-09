import unittest

from pddiansm.thesaurus.ThesauriFiles import ThesauriFiles
from pddiansm.thesaurus.ThesaurusJson import ThesaurusJson
from pddiansm.thesaurus.ThesaurusExceptions import ThesaurusVersionNotFound


class MyTestCase(unittest.TestCase):
    def test_load_thesauri_files(self):
        thesauri_files = ThesauriFiles().thesauri_files
        self.assertEqual(len(thesauri_files), 5)

    def test_singleton(self):
        thesauri_files1 = ThesauriFiles()
        thesauri_files2 = ThesauriFiles()
        self.assertEqual(thesauri_files1, thesauri_files2)

    def test_list_versions(self):
        thesauri_files = ThesauriFiles()
        thesaurus_versions = thesauri_files.get_available_thesaurus_version()
        first_version = thesaurus_versions[0]
        self.assertEqual(first_version, "2016_01")

    def test_version_not_found(self):
        thesauri_files = ThesauriFiles()
        thesaurus_version = "2016_05"
        self.assertRaises(ThesaurusVersionNotFound, thesauri_files.get_thesaurus_files, thesaurus_version)

    def test_found_version(self):
        thesauri_files = ThesauriFiles()
        thesaurus_files = thesauri_files.get_thesaurus_files("2019_09")
        thesaurus = ThesaurusJson(thesaurus_files)
        self.assertIsInstance(thesaurus.pddis, list)
        self.assertEqual(len(thesaurus.pddis), 3035)


if __name__ == '__main__':
    unittest.main()
