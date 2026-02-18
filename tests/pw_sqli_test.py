import copy
import sys
from .playwright_test import PlaywrightTest
from services.error_patterns import match_any


class PlaywrightSQLiTest(PlaywrightTest):
    def test(self):
        passed = 0
        failed = 0
        url = self.domain['protocol'] + self.domain['host'] + self.config['path']
        print("Playwright SQL Injection Test for " + url)
        result_text = []
        result = 'PASS'
        for k, v in self.config['params'].items():
            for p in self.payloads:
                if self.DEBUG: print(url + " param=" + k + " (" + p + ")")
                data = copy.deepcopy(self.config['params'])
                data[k] = data[k] + p

                if self.config['method'] == 'GET':
                    query = '&'.join('{}={}'.format(key, val) for key, val in data.items())
                    test_url = url + '?' + query
                    content, status, console_errors = self.navigate(test_url)
                else:
                    content, status, console_errors = self.fill_and_submit(url, data)

                if status != 200:
                    failed += 1
                    matched = match_any(content, 'sql') or match_any(content, 'generic')
                    if matched:
                        result = 'FAIL'
                        result_text.append('=> Payload ' + p + ' caused a database error in parameter ' + k)
                        sys.stderr.write('=> Payload ' + p + ' caused a database error in parameter ' + k + '\n')
                    else:
                        result = 'ERROR'
                        result_text.append('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
                else:
                    # Check console errors for SQL-related messages
                    for err in console_errors:
                        if match_any(err, 'sql') or match_any(err, 'generic'):
                            failed += 1
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused a console error in parameter ' + k + ': ' + err)
                            break
                    else:
                        passed += 1

            self.report.add_test_result(url, self.config['method'], 'pw-sqli', k, result, result_text)

        self.teardown_browser()
        print("=> " + str(passed) + "/" + str(passed + failed) + " passed/total")
