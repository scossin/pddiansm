# PDDIansm
Scripts to detect Potential Drug Drug Interactions (PDDI) according to the French Agency for the Safety of Health Products (ANSM) guidelines. 

## Examples

### PDDI between two substances:

```python
from pddiansm.detector.PDDIthesaurusDetector import PDDIthesaurusDetector
from pddiansm.thesaurus.ThesauriJson import ThesauriJson

thesaurus = ThesauriJson().get_thesaurus("2019_09")  # thesauri.print_available_thesaurus_version()
pddi_detector = PDDIthesaurusDetector(thesaurus)
substance1 = "domperidone"
substance2 = "escitalopram"
pddis = pddi_detector.detect_pddi(substance1, substance2)
```

## Tests
Run all the tests with this command: 
```bash
python -m unittest discover python
```