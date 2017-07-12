# Regions
An crawler for fetching the latest region of China.

## Compatibility
`python 3`

## Example
```bash
python main.py
```

## How to use
```python
from RegionCrawler import RegionCrawler

crawler = RegionCrawler()
crawler.data  # regions in dict
crawler.to_json()  # json formatted region data
```