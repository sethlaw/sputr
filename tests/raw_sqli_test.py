import re
import copy
import sys
from .raw_requests_test import RawRequestsTest
from services.error_patterns import match_any

class RawSQLiTest(RawRequestsTest):
    def test(self):
        passed = 0
        failed = 0
        messages = []
        url = self.url
        request = self.request
        print("Raw SQL Injection Test for " + url)
        result_text = []
        result = 'PASS'
        sputr_re = re.compile("@@(.*?)##")
        for location in re.finditer(sputr_re,request):
            print(" => " + location.group(0))

            for p in self.payloads:
                print("Payload: %s"%(p))
                req = re.sub(location.group(0),p,request)
                req = re.sub("@@|##","",req)
                res = self.rawrequest(url=url,request=req)
                if res.status_code != 200:
                    failed = failed + 1
                    matched = match_any(res.text, 'sql') or match_any(res.text, 'generic')
                    if matched:
                        result = 'FAIL'
                        result_text.append('=> Payload ' + p + ' caused a database error')
                        sys.stderr.write('=> Payload ' + p + ' caused a database error\n')
                    else:
                        result = 'ERROR'
                        result_text.append('=> Payload ' + p + ' caused an unknown error')
                else:
                    passed = passed + 1


            self.report.add_raw_test_result(url,request,'raw-sqli',res,result,result_text)

        print("=> " + str(passed) + "/" + str(passed + failed) + " passed/total")
