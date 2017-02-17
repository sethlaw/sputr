#base class for all unit test generators
import requests

class Test():
	def __init__(self):
		print("init")

	def __init__(self,config):
		self.config = config
		

	
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
	def get(self,url,params={}):
		print(params)
		return requests.get(url)

	def post(self,url,data={},cookies={}):
		return requests.post(url,data=data,cookies=cookies)

