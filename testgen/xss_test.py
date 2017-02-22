from .basetest import Test
import copy

class xss_test(Test):
	def test(self):
		if self.DEBUG: print("Run the XSS Tests")
		passed = 0
		failed = 0
		messages = []
		url = self.domain['protocol'] + self.domain['host'] + self.config['path']
		for p in self.payloads:
			for k,v in self.config['params'].items():
				if self.DEBUG: print(url + "?" + k + "=" + v + " (" + p + ")")
				if self.config['method'] == 'GET':
					if self.DEBUG: print("Using GET " + self.config['path'])
					data = copy.deepcopy(self.config['params'])
					data[k] = data[k] + p
					res = self.client.get(url,params=data)
					if self.DEBUG: print("Status " + str(res.status_code))
					#if self.DEBUG: print("Content " + str(res.text))
					if p in res.text:
						failed = failed + 1
						print('Payload ' + p + ' not filtered')
					else:
						passed = passed + 1
				elif self.config['method'] == 'POST':
					if self.DEBUG: print("Using POST " + self.config['path'])
					data = copy.deepcopy(self.config['params'])
					data[k] = data[k] + p
					res = self.client.post(url,params=data)
					if self.DEBUG: print("Status " + str(res.status_code))
					#if self.DEBUG: print("Content " + str(res.text))
					if p in res.text:
						failed = failed + 1
						print('Payload ' + p + ' not filtered')
					else:
						passed = passed + 1
				else:
					if self.DEBUG: print("Endpoint method is not GET or POST")
		
		print("XSS Test for " + self.config['path'])
		print("=> " + str(passed) + "/" + str(passed+failed) + " passed/total")
		#print("Messages: " + str(messages))