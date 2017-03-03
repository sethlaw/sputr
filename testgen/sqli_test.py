import re
import copy
from .requests_test import RequestsTest

class SQLiTest(RequestsTest):
	def test(self):
		passed = 0
		failed = 0
		messages = []
		url = self.domain['protocol'] + self.domain['host'] + self.config['path']
		db_pattern = re.compile('database')
		print("SQL Injection Test for " + url)
		
		for p in self.payloads:
			for k,v in self.config['params'].items():
				if self.DEBUG: print(url + "?" + k + "=" + v + " (" + p + ")")
				if self.config['method'] == 'GET':
					if self.DEBUG: print("Using GET " + self.config['path'])
					data = copy.deepcopy(self.config['params'])
					data[k] = data[k] + p
					res = self.get(url,params=data)
					if 'testpath' in self.config:
						res = self.get(self.domain['protocol'] + self.domain['host'] + self.config['testpath'])
					if self.DEBUG: print("Status " + str(res.status_code))
					#if self.DEBUG: print("Content " + str(res.text))
					if res.status_code != 200:
						failed = failed + 1
						if db_pattern.search(res.text,re.IGNORECASE):
							print('=> Payload ' + p + ' caused a database error in paramater ' + k)
						else:
							print('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
					else:
						passed = passed + 1
						
						
				elif self.config['method'] == 'POST':
					data = copy.deepcopy(self.config['params'])
					data[k] = data[k] + p
					if self.DEBUG: print("Using POST " + self.config['path'] + " data: " + str(data))
					res1 = self.get(url) # Get in case we need CSRF tokens and/or other items from the form
					res = self.post(url,data=data)
					if res.status_code != 200:
						failed = failed + 1
						if db_pattern.search(res.text,re.IGNORECASE):
							print('=> Payload ' + p + ' caused a database error in paramater ' + k)
						else:
							print('=> Payload ' + p + ' caused an unknown error in parameter ' + k)
					else:
						passed = passed + 1
				else:
					if self.DEBUG: print("Endpoint method is not GET or POST")
		
		print("=> " + str(passed) + "/" + str(passed+failed) + " passed/total")