from typing import List
from pydantic import BaseModel


class Dosage(BaseModel):
    amount: int
    unit: str


class SubstanceDosage(BaseModel):
    substance: str
    dosage: Dosage


class Drug(BaseModel):
    id: int
    substances: List[SubstanceDosage]
    route: str
    posologie: str  # todo


class Condition(BaseModel):
    icd_10_codes: List[str]


class Patient(BaseModel):
    conditions: List[Condition]


class PatientDrugs(BaseModel):
    drugs: List[Drug]
    patient: Patient


