import requests
import sys
from .requests_test import RequestsTest


class CSRFTest(RequestsTest):

    def execute(self):
        self.post(self.url, self.config["params"], self.cookies)

    def test(self):
        passed = True
        url = self.domain['protocol'] + self.domain['host'] + self.config['path']
        print("CSRF Test for " + url)
        res = self.get(url, params=self.config['params'], allow_redirects=False)

        result_text = []
        result = 'PASS'
        if self.csrf['name'] in res.text:
            if self.config['method'] == 'GET':
                if self.DEBUG: print("*** Using GET " + self.config['path'])
                res = self.get(url, params=self.config['params'], allow_redirects=False)
                res2 = requests.get(url, params=self.config['params'], allow_redirects=False)
                if self.DEBUG: print("csrf status:" + str(res.status_code) + " no token: " + str(res2.status_code))
                if res.status_code == res2.status_code:
                    passed = False

            elif self.config['method'] == 'POST':
                if self.DEBUG: print("*** Using POST " + self.config['path'])
                res = self.post(url, data=self.config['params'], allow_redirects=False)
                res2 = requests.post(url, data=self.config['params'], allow_redirects=False)
                if self.DEBUG: print("csrf status:" + str(res.status_code) + " no token: " + str(res2.status_code))
                if res.status_code == res2.status_code:
                    passed = False

            else:
                if self.DEBUG: print("*** Endpoint method is not GET or POST")

            if not passed:
                sys.stderr.write("=> No csrf validation to " + url + "\n")
                result = 'FAIL'
                result_text.append("=> No csrf validation")

        else:
            result = 'ERROR'
            result_text.append("=> no csrf token found in GET response, bypassing csrf test")

        self.report.add_test_result(url, self.config['method'], 'csrf', 'none', result, result_text)
