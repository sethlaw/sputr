import re
import copy
import sys
from .raw_requests_test import RawRequestsTest

class RawSQLiTest(RawRequestsTest):
    def test(self):
        passed = 0
        failed = 0
        messages = []
        url = self.url
        request = self.request
        db_pattern = re.compile('database|db')
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
                # print(req)
                res = self.rawrequest(url=url,request=req)
                # print(res.headers)
                if res.status_code != 200:
                    failed = failed + 1
                    if db_pattern.search(res.text, re.IGNORECASE):
                        result = 'FAIL'
                        result_text.append('=> Payload ' + p + ' caused a database error')
                        sys.stderr.write('=> Payload ' + p + ' caused a database error\n')
                    else:
                        result = 'ERROR'
                        result_text.append('=> Payload ' + p + ' caused an unknown error')
                else:
                    passed = passed + 1
                

            self.report.add_raw_test_result(url,request,'raw-sqli',res,result,result_text)
                # self.report.add_test_result(url, self.config['method'], 'sqli', k, result, result_text)


       
       #                 if db_pattern.search(res.text, re.IGNORECASE):
       #                     result = 'FAIL'
       #                     result_text.append('=> Payload ' + p + ' caused a database error in parameter ' + k)
       #                     sys.stderr.write('=> Payload ' + p + ' caused a database error in parameter ' + k + '\n')
       #                 else:
       #                     result = 'ERROR'
       #                     result_text.append('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
       #             else:
       #                 passed = passed + 1
       #         else:
       #             if self.DEBUG: print("Endpoint method is not GET or POST")
       #    self.report.add_test_result(url, self.config['method'], 'sqli', k, result, result_text)

        print("=> " + str(passed) + "/" + str(passed + failed) + " passed/total")
