import unittest

from pddiansm.thesaurus.Thesauri import Thesauri
from pddiansm.thesaurus.Thesaurus import Thesaurus


class MyTestCase(unittest.TestCase):
    def test_load_thesaurus(self):
        thesauri = Thesauri()
        thesaurus_version = "2019_09"
        thesaurus = thesauri.get_thesaurus(thesaurus_version)
        self.assertIsInstance(thesaurus, Thesaurus)

    def test_singleton(self):
        thesauri1 = Thesauri()
        thesauri2 = Thesauri()
        self.assertEqual(thesauri1, thesauri2)


if __name__ == '__main__':
    unittest.main()
