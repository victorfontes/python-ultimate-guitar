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



Example
-------
```bash
ultimate-guitar search -q "paranoid android" -t guitar_pro --limit 10 --download 

Usage: ultimate-guitar search [OPTIONS]

Options:
  -q, --query TEXT            The person to greet.
  -t, --filter-type TEXT      Filter results by type
  -l, --limit INTEGER         Limit first N results
  -p, --path TEXT             Path to downloaded files
  --download / --no-download
  --help       

```
