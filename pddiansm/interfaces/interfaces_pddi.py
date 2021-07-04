from typing import List, Dict

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
    parent_drug_classes: List[str]

#### Two majors comments on ClassThesaurus
# 1) why there is no "substances: List[str]" in ClassThesaurus since a drug_class contains substances ?
# when we search PDDI with a drug_class, we don't want to search PDDI for every individual substance that the drug_class contains
# because individual substance can interact on their own
# so there is no "substances: List[str]". Given a drug_class, we search PDDI only at the drug_class level
# 2) what are parent_drug_classes ?
# there are hierarchical relationships between drug_classes. These relationships are not explicitly stated in the document
# For example "diurétiques de l'anse" is a subClassOf "diurétiques hypokaliémants" since all the substances of the former
# are presents in the latter.