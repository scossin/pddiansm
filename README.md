# PDDIansm
A package to detect Potential Drug Drug Interactions (PDDI) according to the French Agency for the Safety of Health Products (ANSM) guidelines. 

## Get started
```bash
pip install ./
```
## Check PDDI between two substances:

```python
from pddiansm.detector.PDDIthesaurusDetector import PDDIthesaurusDetector
from pddiansm.thesaurus.ThesauriJson import ThesauriJson

ThesauriJson().print_available_thesaurus_version()
thesaurus_version = "2019_09"
thesaurus = ThesauriJson().get_thesaurus(thesaurus_version) 
pddi_detector = PDDIthesaurusDetector(thesaurus)
substance1 = "domperidone"
substance2 = "escitalopram"
pddis = pddi_detector.detect_pddi(substance1, substance2)
for pddi in pddis:
    print(pddi)
# domperidone (from 'torsadogenes (sauf arsenieux, antiparasitaires, neuroleptiques, methadone...)') can interact with escitalopram (from 'substances susceptibles de donner des torsades de pointes') in thesaurus version 2019_09
```

## Check PDDI between two simple drugs:
A simple drug is an object, with an id, containing one to many substances. 

```python
from pddiansm.detector.PDDIsimpleDrugsDetector import PDDIsimpleDrugsDetector
from pddiansm.detected.PDDIsimpleDrugsDetected import PDDIsimpleDrugsDetected
from pddiansm.pydantic.interfaces_input import SimpleDrug
from pddiansm.thesaurus.IThesaurus import IThesaurus
from pddiansm.thesaurus.ThesauriJson import ThesauriJson

simple_drug1 = SimpleDrug(id=1, substances=["colchicine", "opium", "tiemonium"])
simple_drug2 = SimpleDrug(id=2, substances=["azithromycine"])
simple_drugs = [simple_drug1, simple_drug2]
thesaurus: IThesaurus = ThesauriJson().get_thesaurus("2019_09")
pddi_detector = PDDIsimpleDrugsDetector(thesaurus)
pddis_detected = pddi_detector.detect_pddi_multiple_drugs(simple_drugs)
for pddi_detected in pddis_detected:
    print(pddi_detected)
# colchicine (from 'colchicine') can interact with azithromycine (from 'macrolides (sauf spiramycine)') in thesaurus version 2019_09. colchicine comes from drug number '1' and azithromycine comes from drug number '2'
```

## Check PDDI between two identifiers:
In case you want to search PDDIs with two identifiers, you need to change the mapper object. For example, between substances: 
```python
from pddiansm.detector.PDDIthesaurusDetector import PDDIthesaurusDetector
from pddiansm.thesaurus.ThesauriJson import ThesauriJson
from pddiansm.detected.PDDIdetected import PDDIdetected
from pddiansm.mapper.AvailableIdentifierMappers import AvailableSubstanceMapping

thesaurus = ThesauriJson().get_thesaurus("2019_09") 
pddi_detector = PDDIthesaurusDetector(thesaurus)
rxnorm_mapper = AvailableSubstanceMapping.RxNorm.value
pddi_detector.set_mapper(rxnorm_mapper)
id_rxnorm_domperidone = "3626"
id_rxnorm_escitalopram = "321988"
pddis_detected = pddi_detector.detect_pddi(id_rxnorm_domperidone, id_rxnorm_escitalopram)
for pddi in pddis_detected:
    print(pddi)
# 3626 (from 'torsadogenes (sauf arsenieux, antiparasitaires, neuroleptiques, methadone...)') can interact with 321988 (from 'substances susceptibles de donner des torsades de pointes') in thesaurus version 2019_09
```
This package contains ANSM substances mappings to Wikidata and RxNorm.


## Tests
Run all the tests with this command: 
```bash
python -m unittest discover ./
```