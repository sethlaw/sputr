import requests
from .requests_test import RequestsTest

class AccessControlTest(RequestsTest):
	def test(self):
		passed = True
		messages = []
		url = self.domain['protocol'] + self.domain['host'] + self.config['path']
		print("Access Control Test for " + url)
		
		if self.config['auth'] == 1:
			if self.config['method'] == 'GET':
				if self.DEBUG: print("*** Using GET " + self.config['path'])
				res = self.get(url,params=self.config['params'],allow_redirects=False)
				res2 = requests.get(url,params=self.config['params'],allow_redirects=False)
				if self.DEBUG: print("auth status:" + str(res.status_code) + " unauth: " + str(res2.status_code))
				if res.status_code == res2.status_code:
					passed = False
				
			elif self.config['method'] == 'POST':
				if self.DEBUG: print("*** Using POST " + self.config['path'])
				res = self.post(url,data=self.config['params'],allow_redirects=False)
				res2 = requests.post(url,data=self.config['params'],allow_redirects=False)
				if self.DEBUG: print("auth status:" + str(res.status_code) + " unauth: " + str(res2.status_code))
				if res.status_code == res2.status_code:
					passed = False
				
			else:
				if self.DEBUG: print("*** Endpoint method is not GET or POST")
			
			if not passed:
				print("=> No auth required for access")
				print("=> 0/1 passed/total")
			else:
				print("=> 1/1 passed/total")
		else:
			print("=> no auth required, bypassing access control test")