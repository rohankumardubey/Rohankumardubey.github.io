#!/usr/bin/env python3
"""Give changed CSS, JavaScript, and favicon files fresh browser-cache URLs.

Run before committing edits to these assets. Files remain buildless; GitHub Pages
serves the same paths and browsers cache each content version separately.
"""

from hashlib import sha256
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ('styles.css', 'script.js', 'favicon.svg')


def version_assets():
    target = ROOT / 'index.html'
    html = target.read_text()
    for name in ASSETS:
        version = sha256((ROOT / name).read_bytes()).hexdigest()[:12]
        pattern = r'(["\'])\./' + re.escape(name) + r'(?:\?v=[^"\']*)?\1'
        html, count = re.subn(pattern, lambda match: f'{match[1]}./{name}?v={version}{match[1]}', html)
        if count != 1:
            raise ValueError(f'Expected one reference to {name}, found {count}')
    target.write_text(html)


if __name__ == '__main__':
    version_assets()
