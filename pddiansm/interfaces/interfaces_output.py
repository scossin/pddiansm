from typing import List

from pydantic import BaseModel

from pddiansm.interfaces.interfaces_input import PatientDrugs
from pddiansm.interfaces.interfaces_pddi import PDDI


class PDDIdetected(BaseModel):
    drug_id_1: int
    substance1: str
    ith_substance_1: int
    drug_id_2: str
    substance2: str
    ith_substance_2: int
    pddi: PDDI


class Thesaurus(BaseModel):
    thesaurus_version: str
    description: str


class APIoutput(BaseModel):
    pddis: List[PDDIdetected]
    thesaurus: Thesaurus
    request: PatientDrugs
