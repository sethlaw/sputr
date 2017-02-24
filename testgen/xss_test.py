from .basetest import Test
import copy

class xss_test(Test):
	def test(self):
		if self.DEBUG: print("Run the XSS Tests")
		passed = 0
		failed = 0
		messages = []
		url = self.domain['protocol'] + self.domain['host'] + self.config['path']
		print("XSS Test for " + url)
		for p in self.payloads:
			for k,v in self.config['params'].items():
				if self.DEBUG: print(url + "?" + k + "=" + v + " (" + p + ")")
				if self.config['method'] == 'GET':
					if self.DEBUG: print("Using GET " + self.config['path'])
					data = copy.deepcopy(self.config['params'])
					data[k] = data[k] + p
					res = self.client.get(url,params=data)
					if 'testpath' in self.config:
						res = self.client.get(self.domain['protocol'] + self.domain['host'] + self.config['testpath'])
					if self.DEBUG: print("Status " + str(res.status_code))
					#if self.DEBUG: print("Content " + str(res.text))
					if p in res.text:
						failed = failed + 1
						print('=> Payload ' + p + ' not filtered for parameter ' + k)
					else:
						passed = passed + 1
				elif self.config['method'] == 'POST':
					data = copy.deepcopy(self.config['params'])
					data[k] = data[k] + p
					if self.DEBUG: print("Using POST " + self.config['path'] + " data: " + str(data))
					res1 = self.client.get(url) # Get in case we need CSRF tokens and/or other items from the form
					res = self.client.post(url,data=data)
					if 'testpath' in self.config:
						res = self.client.get(self.domain['protocol'] + self.domain['host'] + self.config['testpath'])
					if self.DEBUG: print("Status " + str(res.status_code))
					#if self.DEBUG: print("Content " + str(res.text))
					if p in res.text:
						failed = failed + 1
						print('=> Payload ' + p + ' not filtered for parameter ' + k)
					else:
						passed = passed + 1
				else:
					if self.DEBUG: print("Endpoint method is not GET or POST")
		
		print("=> " + str(passed) + "/" + str(passed+failed) + " passed/total")
		#print("Messages: " + str(messages))