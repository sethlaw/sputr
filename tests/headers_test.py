import sys
from .requests_test import RequestsTest

REQUIRED_HEADERS = {
    'Strict-Transport-Security': None,
    'Content-Security-Policy': None,
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': None,
    'Referrer-Policy': None,
}


class HeadersTest(RequestsTest):
    def test(self):
        url = self.domain['protocol'] + self.domain['host'] + self.config['path']
        print("Security Headers Test for " + url)

        res = self.get(url)
        result_text = []
        result = 'PASS'
        passed = 0
        failed = 0

        for header, expected_value in REQUIRED_HEADERS.items():
            actual = res.headers.get(header)
            if actual is None:
                failed += 1
                result = 'FAIL'
                result_text.append('=> Missing header: ' + header)
                sys.stderr.write('=> Missing header: ' + header + '\n')
            elif expected_value and actual.lower() != expected_value.lower():
                failed += 1
                result = 'FAIL'
                result_text.append('=> Incorrect header {}: expected "{}", got "{}"'.format(
                    header, expected_value, actual))
            else:
                passed += 1

        self.report.add_test_result(url, self.config['method'], 'headers', 'none', result, result_text)
        print("=> " + str(passed) + "/" + str(passed + failed) + " passed/total")
