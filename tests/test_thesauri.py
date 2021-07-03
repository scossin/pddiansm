import unittest

from pddiansm.thesaurus.Thesauri import Thesauri
from pddiansm.thesaurus.Thesaurus import Thesaurus


class MyTestCase(unittest.TestCase):
    def test_load_thesaurus(self):
        thesauri = Thesauri()
        thesaurus_version = "2019_09"
        thesaurus = thesauri.get_thesaurus(thesaurus_version)
        self.assertIsInstance(thesaurus, Thesaurus)


if __name__ == '__main__':
    unittest.main()
