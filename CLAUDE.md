# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPUTR (Security Payload Unit Test Repository) is a Python 3 security testing framework that automates penetration testing of web applications. It sends generated payloads against configured endpoints and checks for vulnerabilities: SQLi, XSS, IDOR, CSRF, and Missing Function Level Access Control (MFLAC).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run standard tests against a target app
python3 sputr.py --config config.json --test

# Run raw HTTP request tests
python3 sputr.py --config config.json --raw

# CSRF-only testing
python3 sputr.py --config config.json --testcsrf

# Generate a config template
python3 sputr.py --generate --apptype django --appdir /path/to/app --conf_output config.json

# Verbose output
python3 sputr.py --config config.json --test --verbose
```

There is no linting, type checking, or unit test suite configured for the framework itself.

## Architecture

**Entry point**: `sputr.py` — parses CLI args, loads config, orchestrates test execution.

**Two test modes** with separate base classes:
- `--test`: Standard HTTP via `tests/requests_test.py::RequestsTest` (uses `requests.Session`)
- `--raw`: Raw HTTP via `tests/raw_requests_test.py::RawRequestsTest` (uses `requests_raw`). Raw requests are base64-encoded in config and use `@@payload##` markers for injection points.

**Test classes** (each extends a base class and implements `test()`):
- `tests/sqli_test.py` — SQL injection
- `tests/xss_test.py` — Cross-site scripting
- `tests/idor_test.py` — Insecure direct object reference
- `tests/csrf_test.py` — CSRF protection validation
- `tests/access_control_test.py` — Function-level access control
- `tests/raw_sqli_test.py` — Raw HTTP SQL injection

**Test selection**: The `tests` field in endpoint config is a 5-char binary string where each position maps to a test type: `SQLi|XSS|IDOR|CSRF|MFLAC` (e.g., `"01000"` = XSS only). Raw mode uses string keys like `"raw-sqli"`.

**Services**:
- `services/report_service.py` — Aggregates results (domain → endpoint → param → test results)
- `services/token_service.py` — Extracts CSRF tokens from HTML using BeautifulSoup + regex
- `services/poc_service.py` — Proof-of-concept utilities

**Payload generation** (`generators/payload_generator.py`): Reads character files from `exploit_chars/<type>/` and combines random strings with exploit characters. Payload files live in `payloads/` and `exploit_chars/`.

**Config structure**: JSON with required top-level keys: `token`, `creds`, `csrf`, `domain`, `endpoints`. See `examples/` for sample configs. Raw mode uses `requests` array instead of `endpoints`.

## Key Patterns

- `RequestsTest` auto-authenticates when `config['auth'] == 1` and auto-injects CSRF tokens into POST requests
- The `sputr_tests` dict in `sputr.py` maps test names to `(display_name, payload_path, TestClass)` tuples
- All test classes use the same interface: `__init__` receives config + report + payloads, then `test()` runs the checks
- Results go to a `Report` object passed through the test chain
