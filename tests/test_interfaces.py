import os
import unittest
from typing import List

import importlib.resources as pkg_resources
import pydantic
from pydantic import ValidationError

from pddiansm.pydantic.interfaces_input import SimpleDrug
from pddiansm.pydantic.interfaces_pddi import PDDI, SubstanceThesaurus


def get_path(filename: str) -> str:
    current_dir = os.path.dirname(__file__)
    return current_dir + "/" + filename


class MyTestCase(unittest.TestCase):

    def test_interface_pddi(self):
        package_path = pkg_resources.path("pddiansm", "data")
        with package_path as path:
            filename = str(path) + "/thesauri/2019_09/Thesaurus_09_2019.json"
            pddis = pydantic.parse_file_as(List[PDDI], filename)
            pddi0 = pddis[0]
            self.assertEqual(pddi0.main_drug, "ABATACEPT")
            self.assertEqual(pddi0.between_main_and_plus_drug, "")
            self.assertEqual(pddi0.plus_drug, "ANTI-TNF ALPHA")
            severity_levels0 = pddi0.severity_levels[0]
            self.assertEqual(severity_levels0.level, "Association DECONSEILLEE")
            self.assertEqual(severity_levels0.info, "")
            self.assertEqual(pddi0.interaction_mechanism, "Majoration de l’immunodépression.")
            self.assertEqual(pddi0.description, "Association DECONSEILLEEMajoration de l’immunodépression.")

    def test_interface_substance(self):
        package_path = pkg_resources.path("pddiansm", "data")
        with package_path as path:
            filename = str(path) + "/thesauri/2019_09/index_des_substances_09_2019.json"
            substances = pydantic.parse_file_as(List[SubstanceThesaurus], filename)
            substance1 = substances[1]
            self.assertEqual(substance1.substance, "abciximab (c 7e3b fab)")
            self.assertEqual(substance1.drug_classes, ["antiagrégants plaquettaires", "autres médicaments agissant sur l'hémostase"])

    def test_interface_drug(self):
        path = get_path("data/simple_drugs_test.json")
        try:
            simple_drugs = pydantic.parse_file_as(List[SimpleDrug], path)
        except ValidationError as e:
            self.fail(e)


if __name__ == "__main__":
    unittest.main()
