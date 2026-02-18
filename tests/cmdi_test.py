import re
import copy
import sys
import time
from .requests_test import RequestsTest
from services.error_patterns import match_any


class CmdiTest(RequestsTest):
    def test(self):
        passed = 0
        failed = 0
        url = self.domain['protocol'] + self.domain['host'] + self.config['path']
        print("Command Injection Test for " + url)
        result_text = []
        result = 'PASS'
        for k, v in self.config['params'].items():
            for p in self.payloads:
                if self.DEBUG: print(url + "?" + k + "=" + v + " (" + p + ")")
                if self.config['method'] == 'GET':
                    data = copy.deepcopy(self.config['params'])
                    data[k] = data[k] + p
                    start = time.time()
                    res = self.get(url, params=data)
                    elapsed = time.time() - start
                    if self.DEBUG: print("Status " + str(res.status_code) + " Time: %.2fs" % elapsed)
                    if res.status_code != 200:
                        failed += 1
                        matched = match_any(res.text, 'command') or match_any(res.text, 'generic')
                        if matched:
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused a command error in parameter ' + k)
                            sys.stderr.write('=> Payload ' + p + ' caused a command error in parameter ' + k + '\n')
                        else:
                            result = 'ERROR'
                            result_text.append('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
                    elif elapsed > 10:
                        failed += 1
                        result = 'FAIL'
                        result_text.append('=> Payload ' + p + ' caused a time delay (%.2fs) in parameter ' % elapsed + k)
                    else:
                        passed += 1

                elif self.config['method'] == 'POST':
                    data = copy.deepcopy(self.config['params'])
                    data[k] = data[k] + p
                    res1 = self.get(url)
                    start = time.time()
                    res = self.post(url, data=data)
                    elapsed = time.time() - start
                    if res.status_code != 200:
                        failed += 1
                        matched = match_any(res.text, 'command') or match_any(res.text, 'generic')
                        if matched:
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused a command error in parameter ' + k)
                            sys.stderr.write('=> Payload ' + p + ' caused a command error in parameter ' + k + '\n')
                        else:
                            result = 'ERROR'
                            result_text.append('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
                    elif elapsed > 10:
                        failed += 1
                        result = 'FAIL'
                        result_text.append('=> Payload ' + p + ' caused a time delay (%.2fs) in parameter ' % elapsed + k)
                    else:
                        passed += 1
                else:
                    if self.DEBUG: print("Endpoint method is not GET or POST")
            self.report.add_test_result(url, self.config['method'], 'cmdi', k, result, result_text)

        print("=> " + str(passed) + "/" + str(passed + failed) + " passed/total")
