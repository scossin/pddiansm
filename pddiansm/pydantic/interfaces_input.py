from typing import List
from pydantic import BaseModel


class Dosage(BaseModel):
    amount: int
    unit: str


class Substance(BaseModel):
    substance: str


class SimpleDrug(BaseModel):
    id: int
    substances: List[Substance]




