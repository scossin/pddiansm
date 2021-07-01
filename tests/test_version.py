import unittest

from pddiansm.thesaurus.ThesaurusExceptions import ThesaurusVersionNotFound
from pddiansm.thesaurus.thesaurus import Thesaurus
from pddiansm.thesaurus.versions import Version


class MyTestCase(unittest.TestCase):
    def test_non_instantiable_thesaurus(self):
        self.assertRaises(TypeError, Thesaurus.__init__)

    def test_unfound_version(self):
        version = Version("1998", "inconnu.json", "inconnu.json", "Version inconnu")
        self.assertRaises(ThesaurusVersionNotFound, Thesaurus.get_version, version)

    def test_found_version(self):
        version = Version("092019", "inconnu.json", "inconnu.json", "Version inconnu")
        pddis = Thesaurus.get_version(version)
        self.assertIsInstance(pddis, tuple)
        print(self.assertEqual(len(pddis), 3035))


if __name__ == '__main__':
    unittest.main()
