from typing import List, Dict, Set

from pydantic import BaseModel


class SeverityLevel(BaseModel):
    level: str
    info: str


class PDDI(BaseModel):
    main_drug: str
    between_main_and_plus_drug: str
    plus_drug: str
    severity_levels: List[SeverityLevel]
    interaction_mechanism: str
    description: str


class SubstanceThesaurus(BaseModel):
    substance: str
    drug_classes: List[str]


class ClassThesaurus(BaseModel):
    drug_class: str
    substances: List[str]


class SubstanceClasses(BaseModel):
    hashmap_substances: Dict[str, SubstanceThesaurus]  # map substance to SubstanceThesaurus
    classes: Set[str]