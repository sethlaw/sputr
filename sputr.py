#!/usr/bin/env python3
#####################################
# sputr.py
# created: 2017-01-20
# author: seth
#####################################
import json
import logging
import sys
import argparse
import requests
import requests_raw
import base64
import utils
import re
import registry
from services.report_service import Report
from tests.csrf_test import CSRFTest
from tests.xss_test import XSSTest
from tests.sqli_test import SQLiTest
from tests.access_control_test import AccessControlTest
from tests.idor_test import IDORTest
from tests.raw_sqli_test import RawSQLiTest
from tests.headers_test import HeadersTest
from tests.cmdi_test import CmdiTest
from tests.nosql_test import NoSQLTest
from tests.xml_test import XMLTest
from tests.ldap_test import LDAPTest
from tests.ssi_test import SSITest
from tests.template_test import TemplateTest
from tests.path_traversal_test import PathTraversalTest
from tests.pw_sqli_test import PlaywrightSQLiTest
from tests.pw_xss_test import PlaywrightXSSTest
from generators.payload_generator import Payloads

### Register built-in tests
registry.register('sqli', 'sqli', 'injection/sql', SQLiTest, mode='both')
registry.register('xss', 'xss', 'xss', XSSTest, mode='both')
registry.register('idor', 'idor', None, IDORTest)
registry.register('csrf', 'csrf', None, CSRFTest)
registry.register('bac', 'access control', None, AccessControlTest)
registry.register('raw-sqli', 'sqli', 'injection/sql', RawSQLiTest, transport='raw', mode='both')
registry.register('headers', 'security headers', None, HeadersTest)
registry.register('cmdi', 'command injection', 'injection/command', CmdiTest, mode='both')
registry.register('nosql', 'nosql injection', 'injection/nosql', NoSQLTest, mode='both')
registry.register('xml', 'xml/xpath injection', 'injection/xml', XMLTest, mode='both')
registry.register('ldap', 'ldap injection', 'injection/ldap', LDAPTest, mode='both')
registry.register('ssi', 'ssi injection', 'injection/ssi', SSITest, mode='both')
registry.register('template', 'template injection', 'injection/template', TemplateTest, mode='both')
registry.register('traversal', 'path traversal', 'traversal', PathTraversalTest, mode='both')
registry.register('pw-sqli', 'sqli (browser)', 'injection/sql', PlaywrightSQLiTest, transport='playwright', mode='both', requires_browser=True)
registry.register('pw-xss', 'xss (browser)', 'xss', PlaywrightXSSTest, transport='playwright', mode='both', requires_browser=True)


sys.dont_write_bytecode = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='sputr.py')
    parser.add_argument('--config', dest='config', default='config.json', help='config file (default: config.json)')
    parser.add_argument('--test', action='store_true', help='start tests')
    parser.add_argument('--generate', action='store_true', help='generate config file for app')
    parser.add_argument('--apptype', dest='apptype',
                        help='application type for config generation (django|flask|spring|dotnet)')
    parser.add_argument('--appdir', dest='appdir', help='application directory for config generation')
    parser.add_argument('--conf_output', dest='conf_output', default='config.json',
                        help='file to output config file to')
    parser.add_argument('--output', dest='output', default='results.json', help='file for results output')
    parser.add_argument('--testcsrf', action='store_true', help='test csrf from initial dev')
    parser.add_argument('--raw', action='store_true', help='test a raw request')
    parser.add_argument('--verbose', action='store_true', dest='debug', help='verbose messages')
    parser.add_argument('--list-tests', action='store_true', dest='list_tests', help='list all registered tests')
    parser.add_argument('--only', dest='only', default=None, help='comma-separated list of tests to run (overrides config)')
    parser.add_argument('--format', dest='output_format', default='json', choices=['json', 'text'],
                        help='output format (default: json)')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.list_tests:
        print_registered_tests()
        return 0

    # Patch to SPUTR to allow for raw request tests
    if args.raw:
        c, error = parse_config(args.config)
        if error:
            return error
        try:
            # sputr_re = re.compile("@@(.*?)##")
            for r in c['requests']:
                try:
                    tests = r['tests']
                except (KeyError, TypeError):
                    logger.warning('No tests found for request "%s". Skipping.', r.get('url', 'unknown'))
                    continue
                url = r['url']
                report = Report(url)
                # encoding = c['encoding']
                # Only allows for base64-encoded requests
                request = base64.b64decode(r['request'])
                request = request.decode('ascii')
                for t in r['tests']:
                    entry = registry.get(t)
                    if not entry:
                        logger.warning('Unknown test "%s". Skipping.', t)
                        continue
                    name = entry['display_name']
                    payload = entry['payload_path']
                    runner = entry['test_class']
                    logger.debug('running %s tests', name)
                    payloads = []
                    if payload:
                        payloads = Payloads.generate_payloads(payload, debug=args.debug)
                    test_obj = runner(r, report, url, request, payloads)

                    test_obj.test()

            #with open(args.output, 'w') as f:
            #   json.dump(report.report, f, indent=4)

        except KeyError as e:
            logger.error('Key "%s" not found in configuration.', e)
            return utils.KEY_MISSING

        return 0

    if args.testcsrf or args.test:
        c, error = parse_config(args.config)
        if error:
            return error
        try:
            creds = c['creds']
            domain = c['domain']
            csrf = c['csrf']
            endpoints = c['endpoints']
        except KeyError as e:
            logger.error('Key "%s" not found in configuration.', e)
            return utils.KEY_MISSING

        if args.testcsrf:
            payloads = endpoints[0]['params']  # Refactor this to fit all endpoints
            url = domain['protocol'] + c['domain']['host'] + c['endpoints'][0]['path']
            auth_url = csrf['auth_url']

            with requests.Session() as s:
                res1 = s.post(auth_url, data=creds)  # Authenticate
                res2 = s.post(url, data=payloads)
                if res1.status_code == res2.status_code:
                    logger.warning('TEST FAILED')
        else:
            report = Report(domain['host'])
            only_tests = None
            if args.only:
                only_tests = [t.strip() for t in args.only.split(',')]
            for ep in endpoints:
                try:
                    test_names = registry.resolve_tests(ep['tests'])
                except (KeyError, TypeError):
                    logger.warning('No tests found for endpoint "%s". Skipping.', ep.get('path', 'unknown'))
                    continue
                if only_tests:
                    test_names = [t for t in test_names if t in only_tests]
                for test_name in test_names:
                    entry = registry.get(test_name)
                    if not entry:
                        logger.warning('Unknown test "%s". Skipping.', test_name)
                        continue
                    if entry['requires_browser']:
                        try:
                            import playwright
                        except ImportError:
                            logger.warning('Playwright not installed. Skipping %s test.', test_name)
                            continue
                    name = entry['display_name']
                    payload = entry['payload_path']
                    runner = entry['test_class']
                    mode = entry['mode']
                    logger.debug('running %s tests', name)
                    payloads = []
                    if payload:
                        payloads = Payloads.generate_payloads(payload, mode=mode, debug=args.debug)
                    test_obj = runner(ep, report, domain, creds, csrf, payloads, DEBUG=args.debug)
                    test_obj.test()

            if args.output_format == 'text':
                print_text_report(report)
            else:
                print(json.dumps(report.report, indent=4, default=str))
            with open(args.output, 'w') as f:
                json.dump(report.report, f, indent=4, default=str)
    elif args.generate:
        print('generating config from {0} as a {1} application to {2}'.format(args.appdir, args.apptype, args.conf_output))
        generate_config(args.appdir, args.apptype, args.conf_output)
    else:
        parser.print_help()
    return 0


def print_registered_tests():
    all_tests = registry.get_all()
    print('{:<15} {:<20} {:<12} {:<10}'.format('Name', 'Display Name', 'Transport', 'Payloads'))
    print('-' * 60)
    for name, entry in sorted(all_tests.items()):
        transport = entry['transport']
        if entry['requires_browser']:
            transport += ' (browser)'
        payload = entry['payload_path'] or 'none'
        print('{:<15} {:<20} {:<12} {:<10}'.format(name, entry['display_name'], transport, payload))


def print_text_report(report):
    data = report.report
    print('=' * 60)
    print('SPUTR Test Results - {}'.format(data.get('domain', '')))
    print('=' * 60)

    severity_map = {
        'sqli': 'CRITICAL', 'raw-sqli': 'CRITICAL', 'cmdi': 'CRITICAL',
        'nosql': 'HIGH', 'xml': 'HIGH', 'ldap': 'HIGH', 'ssi': 'HIGH',
        'template': 'HIGH', 'traversal': 'HIGH',
        'xss': 'HIGH', 'csrf': 'MEDIUM', 'idor': 'HIGH',
        'access_control': 'HIGH', 'bac': 'HIGH',
        'headers': 'LOW',
    }

    summary = {'PASS': 0, 'FAIL': 0, 'ERROR': 0}

    for endpoint, params in data.get('endpoints', {}).items():
        print('\n  Endpoint: {}'.format(endpoint))
        for param, tests in params.items():
            for test_name, result in tests.items():
                status = result.get('result', 'UNKNOWN')
                severity = severity_map.get(test_name, 'MEDIUM')
                summary[status] = summary.get(status, 0) + 1
                marker = 'PASS' if status == 'PASS' else '{} [{}]'.format(status, severity)
                print('    [{}] {} / param={}'.format(marker, test_name, param))
                for txt in result.get('result_text', []):
                    print('      {}'.format(txt))

    for url, tests in data.get('urls', {}).items():
        print('\n  URL: {}'.format(url))
        for test_name, entries in tests.items():
            for entry in entries:
                status = entry.get('result', 'UNKNOWN')
                summary[status] = summary.get(status, 0) + 1
                print('    [{}] {}'.format(status, test_name))

    print('\n' + '=' * 60)
    print('Summary: {} PASS, {} FAIL, {} ERROR'.format(
        summary.get('PASS', 0), summary.get('FAIL', 0), summary.get('ERROR', 0)))
    print('=' * 60)


def generate_config(appdir, apptype, output):
    config = {
        'token': {
            'name': 'cookie_name',
            'value': 'cookie_value',
        },
        'creds': {
            'username': {
                'name': 'username',
                'value': 'testuser',
            },
            'password': {
                'name': 'password',
                'password': 'temppass',
            },
        },
        'csrf': {
            'pattern': '^regexpattern$',
            'name': 'csrftokenname',

        },
        'domain': {
            'host': 'localhost:8000',
            'protocol': 'http://',
            'login_url': 'http://localhost:8000/taskManager/login',
            'auth_url': 'http://localhost:8000/taskManager/dashboard',
        },
        'endpoints': [
            {
                'path': '/',
                'method': 'GET',
                'auth': 0,
                'params': {},
                'tests': ['sqli', 'xss', 'idor', 'csrf', 'bac'],
            },
        ],
    }
    if apptype == 'django':
        print('adding django endpoints')
    # TODO django parsing
    elif apptype == 'java':
        print('adding java spring endpoints')
    # TODO java spring parsing
    elif apptype == 'dotnet':
        print('adding dotnet mvc endpoints')
    # TODO dotnet mvc parsing
    elif apptype == 'flask':
        print('adding flask endpoints')
    # TODO flask parsing
    with open(output, 'w') as f:
        json.dump(config, f, indent=4)


def parse_config(f):
    d = None
    error = None
    try:
        with open(f, 'r') as config:
            d = json.loads(config.read())
    except FileNotFoundError:
        logger.error('Error: Configuration file "%s" not found.', f)
        error = utils.CONFIG_NOT_FOUND
    except json.decoder.JSONDecodeError:
        logger.error('Error: Configuration file "%s" is not a valid JSON file.', f)
        error = utils.CONFIG_INVALID
    return d, error


if __name__ == '__main__':
    sys.exit(main())
