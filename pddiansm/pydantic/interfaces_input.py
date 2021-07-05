from typing import List
from pydantic import BaseModel


class SimpleDrug(BaseModel):
    id: int
    substances: List[str]




