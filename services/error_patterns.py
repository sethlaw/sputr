#!/usr/bin/env python3
#####################################
# error_patterns.py
# Shared error detection patterns
#####################################

import re

ERROR_PATTERNS = {
    'sql': [
        r'database',
        r'sql.*syntax',
        r'mysql.*error',
        r'ORA-\d{5}',
        r'pg_query',
        r'SQLSTATE',
        r'sqlite3\.',
        r'Microsoft.*ODBC',
        r'unclosed quotation',
    ],
    'nosql': [
        r'MongoError',
        r'bson',
        r'ObjectId',
    ],
    'command': [
        r'sh:',
        r'command not found',
        r'syntax error near',
        r'/bin/',
        r'cannot execute',
    ],
    'xml': [
        r'XML.*pars(e|ing)',
        r'SAXParse',
        r'lxml\.etree',
        r'not well-formed',
    ],
    'path': [
        r'No such file',
        r'FileNotFoundError',
        r'open_basedir',
        r'Permission denied',
    ],
    'ldap': [
        r'LDAP error',
        r'Invalid DN',
        r'filter error',
        r'ldap_search',
    ],
    'ssi': [
        r'SSI error',
        r'an error occurred while processing this directive',
        r'fsize',
    ],
    'template': [
        r'TemplateSyntaxError',
        r'Jinja2',
        r'UndefinedError',
        r'Twig.*Error',
    ],
    'generic': [
        r'stack\s*trace',
        r'Traceback',
        r'Exception',
        r'Internal Server Error',
        r'Fatal error',
    ],
}

# Pre-compiled patterns for each category
_compiled = {}


def get_patterns(category):
    """Get compiled regex patterns for a category.

    Returns a list of compiled regex patterns.
    """
    if category not in _compiled:
        _compiled[category] = [re.compile(p, re.IGNORECASE) for p in ERROR_PATTERNS.get(category, [])]
    return _compiled[category]


def match_any(text, category):
    """Check if text matches any pattern in the given category.

    Returns the first matching pattern string, or None.
    """
    patterns = ERROR_PATTERNS.get(category, [])
    for i, compiled in enumerate(get_patterns(category)):
        if compiled.search(text):
            return patterns[i]
    return None


def match_categories(text, categories):
    """Check text against multiple categories.

    Returns a dict of {category: matched_pattern} for categories that matched.
    """
    results = {}
    for cat in categories:
        match = match_any(text, cat)
        if match:
            results[cat] = match
    return results
