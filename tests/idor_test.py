import sys
from .requests_test import RequestsTest


class IDORTest(RequestsTest):
    def test(self):
        if self.DEBUG: print("Run the IDOR Tests")
        passed = True
        failed = 0
        result = 'PASS'
        result_text = []
        messages = []
        url = self.domain['protocol'] + self.domain['host'] + self.config['path']
        testurl = self.domain['protocol'] + self.domain['host'] + self.config['idorpath']
        print("IDOR Test for " + url)

        if self.config['method'] == 'GET':
            if self.DEBUG: print("*** Using GET " + self.config['path'])
            res = self.get(url, params=self.config['params'], allow_redirects=False)
            res2 = self.get(testurl, params=self.config['params'], allow_redirects=False)
            if self.DEBUG: print("idor status:" + str(res.status_code) + " test: " + str(res2.status_code))
            if self.config['teststring'] in res2.text:
                passed = False

        elif self.config['method'] == 'POST':
            if self.DEBUG: print("*** Using POST " + self.config['path'])
            res = self.post(url, params=self.config['params'], allow_redirects=False)
            res2 = self.post(testurl, params=self.config['params'], allow_redirects=False)
            if self.DEBUG: print("idor status:" + str(res.status_code) + " test: " + str(res2.status_code))
            if self.config['teststring'] in res2.text:
                passed = False

        else:
            if self.DEBUG: print("*** Endpoint method is not GET or POST")

        if not passed:
            sys.stderr.write("=> IDOR found at " + url + "\n")
            result = 'FAIL'
            result_text.append("=> No authorization required for data access")

        self.report.add_test_result(url, self.config['method'], 'idor', 'none', result, result_text)
