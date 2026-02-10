"""
CGI module compatibility fix for Python 3.13+
This is a minimal replacement for the removed cgi module
"""
import html
from urllib.parse import parse_qs


def escape(s, quote=True):
    """Replace special characters with HTML entities."""
    return html.escape(s, quote=quote)


def parse_header(line):
    """Parse a Content-type like header."""
    parts = line.split(';')
    key = parts[0].strip()
    pdict = {}
    for p in parts[1:]:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i+1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict


# Add to sys.modules so feedparser can find it
import sys
sys.modules['cgi'] = sys.modules[__name__]
