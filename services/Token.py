import requests
import re



class TokenGenerationService():

	def __init__(self,config):
		self.cookies = config["token"]
		self.creds = config["creds"]
		self.csrf = config["csrf"]
		

	def login(self):
		return requests.post(self.csrf["auth_url"],data=self.creds, cookies=self.cookies)

	def getSessionCookie(self):
		response = self.login()
		return response.cookies.get_dict()[self.cookies["name"]]
	
	def getAuthHeader(self):
		#This is for Auth based Authn Strategies
		return

		#Get Specified header Value
	def getCSRFToken(self):
		r = requests.get(self.csrf["login_url"])
		self.cookies[self.cookies["name"]] = r.cookies.get_dict()[self.cookies["name"]]
		tokens = re.findall(self.csrf["pattern"],r.text)
		return tokens[0]

