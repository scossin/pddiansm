import os
import unittest
from typing import List

import pydantic
from pydantic import ValidationError

from pddiansm.interfaces.interfaces_input import PatientDrugs
from pddiansm.interfaces.interfaces_output import APIoutput
from pddiansm.interfaces.interfaces_pddi import PDDI, SubstanceThesaurus


def get_path(filename: str) -> str:
    current_dir = os.path.dirname(__file__)
    return current_dir + "/" + filename


class MyTestCase(unittest.TestCase):
    def test_interface_pddi(self):
        path = get_path("../pddiansm/thesaurus/thesaurus_092019.json")
        pddis = pydantic.parse_file_as(List[PDDI], path)
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
        path = get_path("../pddiansm/thesaurus/index_substances092019.json")
        substances = pydantic.parse_file_as(List[SubstanceThesaurus], path)
        substance1 = substances[1]
        self.assertEqual(substance1.substance, "abciximab (c 7e3b fab)")
        self.assertEqual(substance1.drug_classes, ["antiagrégants plaquettaires"])

    def test_interface_drug(self):
        path = get_path("../pddiansm/interfaces/patient_drugs_tests.json")
        try:
            patient_drugs = pydantic.parse_file_as(PatientDrugs, path)
        except ValidationError as e:
            self.fail(e)

    def test_interface_output(self):
        path = get_path("../pddiansm/interfaces/api_output_tests.json")
        try:
            api_output = pydantic.parse_file_as(APIoutput, path)
        except ValidationError as e:
            self.fail(e)


if __name__ == "__main__":
    unittest.main()
