python-ultimate-guitar
==============

python bindings for ultimate-guitar.com

Supports:
----------
- search with type filtering (pro, tab, chords, etc)
- dowload tabs and guitar pro files


Example
-------
```python
from ultimate_guitar import UltimateGuitarScraper
ug = UltimateGuitarScraper()
ug.search('paranoid android')
>>> <ResultSet: paranoid android returned 28 results>

ug.search('paranoid android', filter_type='guitar_pro')
<ResultSet: paranoid android returned 9 results>

```
