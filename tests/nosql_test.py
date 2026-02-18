import copy
import sys
from .requests_test import RequestsTest
from services.error_patterns import match_any


class NoSQLTest(RequestsTest):
    def test(self):
        passed = 0
        failed = 0
        url = self.domain['protocol'] + self.domain['host'] + self.config['path']
        print("NoSQL Injection Test for " + url)
        result_text = []
        result = 'PASS'

        # Get baseline response for comparison
        baseline = self.get(url, params=self.config['params'])
        baseline_len = len(baseline.text)

        for k, v in self.config['params'].items():
            for p in self.payloads:
                if self.DEBUG: print(url + "?" + k + "=" + v + " (" + p + ")")
                if self.config['method'] == 'GET':
                    data = copy.deepcopy(self.config['params'])
                    data[k] = data[k] + p
                    res = self.get(url, params=data)
                    if self.DEBUG: print("Status " + str(res.status_code))
                    if res.status_code != 200:
                        failed += 1
                        matched = match_any(res.text, 'nosql') or match_any(res.text, 'generic')
                        if matched:
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused a NoSQL error in parameter ' + k)
                            sys.stderr.write('=> Payload ' + p + ' caused a NoSQL error in parameter ' + k + '\n')
                        else:
                            result = 'ERROR'
                            result_text.append('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
                    else:
                        # Check for significant response body difference (data leak)
                        diff_ratio = abs(len(res.text) - baseline_len) / max(baseline_len, 1)
                        if diff_ratio > 0.5 and baseline_len > 100:
                            failed += 1
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused significant response change in parameter ' + k)
                        else:
                            passed += 1

                elif self.config['method'] == 'POST':
                    data = copy.deepcopy(self.config['params'])
                    data[k] = data[k] + p
                    res1 = self.get(url)
                    res = self.post(url, data=data)
                    if res.status_code != 200:
                        failed += 1
                        matched = match_any(res.text, 'nosql') or match_any(res.text, 'generic')
                        if matched:
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused a NoSQL error in parameter ' + k)
                            sys.stderr.write('=> Payload ' + p + ' caused a NoSQL error in parameter ' + k + '\n')
                        else:
                            result = 'ERROR'
                            result_text.append('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
                    else:
                        diff_ratio = abs(len(res.text) - baseline_len) / max(baseline_len, 1)
                        if diff_ratio > 0.5 and baseline_len > 100:
                            failed += 1
                            result = 'FAIL'
                            result_text.append('=> Payload ' + p + ' caused significant response change in parameter ' + k)
                        else:
                            passed += 1
                else:
                    if self.DEBUG: print("Endpoint method is not GET or POST")
            self.report.add_test_result(url, self.config['method'], 'nosql', k, result, result_text)

        print("=> " + str(passed) + "/" + str(passed + failed) + " passed/total")
