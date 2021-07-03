# PDDIansm
Scripts to detect Potential Drug Drug Interactions (PDDI) according to the French Agency for the Safety of Health Products (ANSM)

## Examples

### PDDI between two substances:
```python
thesaurus = Thesauri().get_thesaurus("2019_09") # thesauri.print_available_thesaurus_version()
pddi_detector = PDDIansmDetector(thesaurus)
substance1 = "domperidone"
substance2 = "escitalopram"
pddis = pddi_detector.detect_pddi(substance1, substance2)
```

## Tests
Run all the tests with this command: 
```bash
python -m unittest discover python
```