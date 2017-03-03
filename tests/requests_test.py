#base class for all unit test generators
import requests
import unittest

from services.token_service import TokenService

class RequestsTest(unittest.TestCase):
	
	def __init__(self):
		print("init")

	def __init__(self,config,domain={},creds={},csrf={},payloads=[],DEBUG=False):
		self.client = requests.Session() # Each Test gets it's own session
		self.config = config
		self.creds = creds
		self.domain = domain
		self.payloads = payloads
		self.csrf = csrf
		self.DEBUG=DEBUG
		self.csrftoken = ""
		self.token_service = TokenService(self.csrf)
		if config['auth'] == 1:
			self.authenticate()

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
		res = self.client.get(url,params=params,cookies=cookies)
		tmptoken = self.token_service.getCSRFToken(res.text,self.DEBUG)
		if tmptoken != "":
			self.csrftoken = tmptoken
		return res

	def post(self,url,data={},cookies={}):
		if self.DEBUG: print(url + " : " + str(data) + " : " + str(cookies))
		if self.csrftoken != "":
			data[self.csrf['name']] = self.csrftoken
			#print("Adding csrf token to post " + self.csrftoken)
		#else:
			#print("No csrf token to post " + self.csrftoken)
		res = self.client.post(url,data=data,cookies=cookies)
		tmptoken = self.token_service.getCSRFToken(res.text,self.DEBUG)
		if tmptoken != "":
			self.csrftoken = tmptoken
		return res
	
	def authenticate(self):
		if self.DEBUG: print("authenticating as " + self.creds['username']['value'] + " to " + self.domain['login_url'] )
		res1 = self.get(self.domain['login_url'])
		if self.DEBUG: print("Status: " + str(res1.status_code))

		data = { self.creds['username']['name']: self.creds['username']['value'],
				self.creds['password']['name']: self.creds['password']['password'] }
		res2 = self.post(self.domain['login_url'],data=data)
		if self.DEBUG: print("Status: " + str(res2.status_code))
		
		res3 = self.get(self.domain['auth_url'])
		if self.DEBUG: print("Status: " + str(res3.status_code))
		
		return res2.status_code

