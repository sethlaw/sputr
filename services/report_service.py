from datetime import datetime
import base64
import logging
import utils

logger = logging.getLogger(__name__)



class Report:
    def __init__(self, domain):
        self.report = {'domain': domain, 'endpoints': {}, 'urls': {}}

    def add_test_result(self, endpoint, method, test, param, result, result_text):
        if endpoint not in self.report['endpoints'].keys():
            self.report['endpoints'][endpoint] = {}
        if param not in self.report['endpoints'][endpoint].keys():
            self.report['endpoints'][endpoint][param] = {}
        if test not in self.report['endpoints'][endpoint][param].keys():
            self.report['endpoints'][endpoint][param][test] = {}

        self.report['endpoints'][endpoint][param][test] = {
            'method': method,
            'result': result,
            'date': datetime.now().isoformat(),
            'result_text': result_text,
        }
    
    def add_raw_test_result(self, url, request, test, response, result, result_text):
        try: 
            if url not in self.report['urls'].keys():
                self.report['urls'][url] = {}
            if test not in self.report['urls'][url].keys():
                self.report['urls'][url][test] = []

            text_response = str(response.status_code) + " " + response.reason + "\n" + str(response.headers) + "\n" + response.text
            self.report['urls'][url][test].append({
                'request': base64.b64encode(bytes(request, 'utf-8')),
                'result': result,
                'response': base64.b64encode(bytes(text_response,'utf-8')),
                'date': datetime.now().isoformat(),
                'result_text': result_text,
            })
        except KeyError as e:
            logger.error('Key "%s" not found in report.', e)
            return utils.KEY_MISSING
