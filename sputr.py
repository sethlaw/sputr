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
import utils
from services.report_service import Report
from tests.csrf_test import CSRFTest
from tests.xss_test import XSSTest
from tests.sqli_test import SQLiTest
from tests.access_control_test import AccessControlTest
from tests.idor_test import IDORTest
from generators.payload_generator import Payloads


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
    parser.add_argument('--verbose', action='store_true', dest='debug', help='verbose messages')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

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
            report = Report(domain)
            for ep in endpoints:
                try:
                    tests = list(ep['tests'])
                except (KeyError, TypeError):
                    logger.warning('No tests found for endpoint "%s". Skipping.', ep.get('path', 'unknown'))
                    continue
                test_runner_configs = [
                    ('sqli', 'injection/sql', SQLiTest),
                    ('xss', 'xss', XSSTest),
                    ('idor', None, IDORTest),
                    ('csrf', None, CSRFTest),
                    ('access control', None, AccessControlTest),
                ]
                for i, (name, payload, runner) in enumerate(test_runner_configs, 1):
                    if tests[i-1] != '1':  # test not activated
                        continue
                    logger.debug('running %s tests', name)
                    payloads = []
                    if payload:
                        payloads = Payloads.generate_payloads(payload, debug=args.debug)
                    test_obj = runner(ep, report, domain, creds, csrf, payloads, DEBUG=args.debug)
                    test_obj.test()

            with open(args.output, 'w') as f:
                json.dump(report.report, f, indent=4)
    elif args.generate:
        print('generating config from {0} as a {1} application to {2}'.format(args.app_dir, args.apptype, args.output))
        generate_config(args.appdir, args.apptype, args.conf_output)
    else:
        parser.print_help()
    return 0


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
                'tests': "11111",
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
