import copy
import sys
from .playwright_test import PlaywrightTest
from services.error_patterns import match_any


class PlaywrightXSSTest(PlaywrightTest):
    def test(self):
        passed = 0
        failed = 0
        url = self.domain['protocol'] + self.domain['host'] + self.config['path']
        print("Playwright XSS Test for " + url)
        for k, v in self.config['params'].items():
            result_text = []
            result = 'PASS'
            for p in self.payloads:
                if self.DEBUG: print(url + " param=" + k + " (" + p + ")")
                data = copy.deepcopy(self.config['params'])
                data[k] = data[k] + p

                if self.config['method'] == 'GET':
                    query = '&'.join('{}={}'.format(key, val) for key, val in data.items())
                    test_url = url + '?' + query
                    content, status, console_errors = self.navigate(test_url)
                    if 'testpath' in self.config:
                        content, status, console_errors = self.navigate(
                            self.domain['protocol'] + self.domain['host'] + self.config['testpath'])
                else:
                    content, status, console_errors = self.fill_and_submit(url, data)
                    if 'testpath' in self.config:
                        content, status, console_errors = self.navigate(
                            self.domain['protocol'] + self.domain['host'] + self.config['testpath'])

                if status != 200:
                    result_text.append('Payload ' + p + ' caused an unknown error for parameter ' + k)
                    failed += 1
                    result = 'ERROR'
                elif p in content:
                    failed += 1
                    result = 'FAIL'
                    result_text.append('=> Payload ' + p + ' not filtered for parameter ' + k)
                    sys.stderr.write('=> Payload ' + p + ' not filtered for parameter ' + k + '\n')
                else:
                    # Check console for JS errors triggered by fuzz input
                    for err in console_errors:
                        if match_any(err, 'generic'):
                            failed += 1
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused a console error in parameter ' + k + ': ' + err)
                            break
                    else:
                        passed += 1

            self.report.add_test_result(url, self.config['method'], 'pw-xss', k, result, result_text)

        self.teardown_browser()
        print("=> " + str(passed) + "/" + str(passed + failed) + " passed/total")
