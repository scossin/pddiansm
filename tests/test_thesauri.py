import unittest

from pddiansm.thesaurus.IThesauri import IThesauri
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.ThesauriJson import ThesauriJson


class MyTestCase(unittest.TestCase):
    def test_load_thesaurus(self):
        thesauri: IThesauri = ThesauriJson()
        thesaurus_version = "2019_09"
        thesaurus: IThesaurus = thesauri.get_thesaurus(thesaurus_version)
        self.assertIsInstance(thesaurus, IThesaurus)

    def test_singleton(self):
        thesauri1: IThesauri = ThesauriJson()
        thesauri2: IThesauri = ThesauriJson()
        self.assertEqual(thesauri1, thesauri2)


if __name__ == '__main__':
    unittest.main()
