#base class for all unit test generators
import requests
import unittest

class Test(unittest.TestCase):
	
	def __init__(self):
		print("init")

	def __init__(self,config,domain={},creds={},payloads=[],DEBUG=False):
		self.client = requests.Session() # Each Test gets it's own session
		self.config = config
		self.creds = creds
		self.domain = domain
		self.payloads = payloads
		self.DEBUG=DEBUG
		if config['auth'] == 1:
			self.authenticate()
	
	def get_payloads(self):
		print("payloads")
		#make a call to "generate_payloads.py" and get the appropriate payloads

	def setUp(self):
		return
		#do setup

	def tearDown(self):
		return
		#do tear down

	def mockService(self):
		return
		
	#Send an HTTP GET Request, wrapper around python requests library.
	#Returns a Response object
	def get(self,url,params={},cookies={}):
		if self.DEBUG: print(url + " : " + str(params) + " : " + str(cookies))
		return self.client.get(url,params=params)

	def post(self,url,data={},cookies={}):
		if self.DEBUG: print(url + " : " + str(data) + " : " + str(cookies))
		return self.client.post(url,data=data,cookies=cookies)
	
	def authenticate(self):
		if self.DEBUG: print("authenticating as " + self.creds['username']['value'] + " to " + self.domain['login_url'] )
		res1 = self.client.get(self.domain['login_url'])
		if self.DEBUG: print("Status: " + str(res1.status_code))
		#if self.DEBUG: print("Status: " + str(res1.text))
		data = { self.creds['username']['name']: self.creds['username']['value'],
				self.creds['password']['name']: self.creds['password']['password'] }
		res2 = self.client.post(self.domain['login_url'],data=data)
		if self.DEBUG: print("Status: " + str(res2.status_code))
		#if self.DEBUG: print("Headers: " + str(res2.headers))
		#if self.DEBUG: print("Content: " + str(res2.text))
		res3 = self.client.get(self.domain['auth_url'])
		if self.DEBUG: print("Status: " + str(res3.status_code))
		#if self.DEBUG: print("Content: " + str(res3.text))
		return res2.status_code

