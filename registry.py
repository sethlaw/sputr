#!/usr/bin/env python3
#####################################
# registry.py
# Test registry for SPUTR
#####################################

# Maps position index in legacy binary test string to test name
LEGACY_TEST_POSITIONS = ['sqli', 'xss', 'idor', 'csrf', 'bac']

_registry = {}


def register(name, display_name, payload_path, test_class, transport='requests', mode='chars', requires_browser=False):
    _registry[name] = {
        'name': name,
        'display_name': display_name,
        'payload_path': payload_path,
        'test_class': test_class,
        'transport': transport,
        'mode': mode,
        'requires_browser': requires_browser,
    }


def get(name):
    return _registry.get(name)


def get_all():
    return dict(_registry)


def resolve_tests(tests_value):
    """Convert a tests config value to a list of test names.

    Supports both:
      - Legacy binary string: "01000" -> ["xss"]
      - Named list: ["sqli", "xss"] -> ["sqli", "xss"]
    """
    if isinstance(tests_value, list):
        return tests_value
    if isinstance(tests_value, str):
        result = []
        for i, ch in enumerate(tests_value):
            if ch == '1' and i < len(LEGACY_TEST_POSITIONS):
                result.append(LEGACY_TEST_POSITIONS[i])
        return result
    return []
