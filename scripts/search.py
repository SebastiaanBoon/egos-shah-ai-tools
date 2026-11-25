"""Search the catalog offline; no third-party dependencies."""
import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / 'data' / 'catalog.json'


def load_catalog():
    return json.loads(CATALOG.read_text(encoding='utf-8'))


def search(items, query='', category='', access=''):
    terms = query.casefold().split()
    return [item for item in items
            if all(term in ' '.join(item.values()).casefold() for term in terms)
            and (not category or item['category'].casefold() == category.casefold())
            and (not access or item['access'].casefold() == access.casefold())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--category', default='')
    parser.add_argument('--access', default='')
    parser.add_argument('--list-categories', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    items = load_catalog()
    if args.list_categories:
        print('\n'.join(sorted({item['category'] for item in items})))
        return
    matches = search(items, args.query, args.category, args.access)
    if args.json:
        print(json.dumps(matches, indent=2, ensure_ascii=False))
    else:
        for item in matches:
            print(f"{item['name']} [{item['access']}] — {item['url']}\n  {item['description']}")
        print(f'{len(matches)} matches')


if __name__ == '__main__':
    main()
