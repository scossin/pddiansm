import unittest

from pddiansm.thesaurus.ThesauriJson import ThesauriJson
from pddiansm.thesaurus.ThesaurusJson import ThesaurusJson


class MyTestCase(unittest.TestCase):
    def test_load_thesaurus(self):
        thesauri = ThesauriJson()
        thesaurus_version = "2019_09"
        thesaurus = thesauri.get_thesaurus(thesaurus_version)
        self.assertIsInstance(thesaurus, ThesaurusJson)

    def test_singleton(self):
        thesauri1 = ThesauriJson()
        thesauri2 = ThesauriJson()
        self.assertEqual(thesauri1, thesauri2)


if __name__ == '__main__':
    unittest.main()
