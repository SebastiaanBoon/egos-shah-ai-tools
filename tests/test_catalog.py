import json
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from search import load_catalog, search


class CatalogTests(unittest.TestCase):
    def test_schema_and_unique_names(self):
        items = load_catalog()
        self.assertGreaterEqual(len(items), 60)
        names = set()
        for item in items:
            self.assertEqual(set(item), {'category', 'name', 'url', 'access', 'description'})
            self.assertTrue(all(isinstance(v, str) and v.strip() for v in item.values()))
            self.assertNotIn(item['name'].casefold(), names)
            names.add(item['name'].casefold())
            url = urlparse(item['url'])
            self.assertEqual(url.scheme, 'https')
            self.assertTrue(url.hostname)

    def test_filters(self):
        items = load_catalog()
        self.assertEqual(search(items, 'OLLAMA')[0]['name'], 'Ollama')
        matches = search(items, category='local models', access='local')
        self.assertTrue(matches)
        self.assertTrue(all(i['access'] == 'Local' for i in matches))
        self.assertEqual(search(items, 'nonexistent-tool-xyz'), [])

    def test_cli_json(self):
        out = subprocess.check_output([sys.executable, str(ROOT / 'scripts/search.py'), '--category', 'Coding', '--json'], text=True)
        self.assertTrue(all(i['category'] == 'Coding' for i in json.loads(out)))

    def test_readme_contains_catalog(self):
        readme = (ROOT / 'README.md').read_text()
        for item in load_catalog():
            self.assertIn(f"[{item['name']}]({item['url']})", readme)
