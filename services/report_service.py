from datetime import datetime

class Report():
	def __init__(self,domain):
		self.report = {}
		self.report['domain'] = domain
		self.report['endpoints'] = {}
		
	def add_test_result(self,endpoint,method,test,param,result,result_text):
		if endpoint not in self.report['endpoints'].keys():
			self.report['endpoints'][endpoint] = {}
		if param not in self.report['endpoints'][endpoint].keys():
			self.report['endpoints'][endpoint][param] = {}
		if test not in self.report['endpoints'][endpoint][param].keys():
			self.report['endpoints'][endpoint][param][test] = {}
		
		self.report['endpoints'][endpoint][param][test]['method'] = method
		self.report['endpoints'][endpoint][param][test]['result'] = result
		self.report['endpoints'][endpoint][param][test]['date'] = datetime.now().isoformat()
		self.report['endpoints'][endpoint][param][test]['result_text'] = result_text