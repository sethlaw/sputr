from datetime import datetime


class Report:
    def __init__(self, domain):
        self.report = {'domain': domain, 'endpoints': {}}

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
