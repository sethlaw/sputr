import requests
import re
from bs4 import BeautifulSoup

class TokenService():

	def __init__(self,csrf):
		self.csrf = csrf
		

	def login(self):
		return requests.post(self.csrf["auth_url"],data=self.creds, cookies=self.cookies)

	def getSessionCookie(self):
		response = self.login()
		return response.cookies.get_dict()[self.cookies["name"]]
	
	def getAuthHeader(self):
		#This is for Auth based Authn Strategies
		return

		#Get Specified header Value
	def getCSRFToken(self,html,DEBUG=False):
		soup = BeautifulSoup(html,"lxml")
		c = soup.find('input',{"name":self.csrf['name']})
		if c:
			if re.match(self.csrf['pattern'],c['value']):
				return c['value']

		#print("No CSRF Token found")
		return ""
		#r = requests.get(self.csrf["login_url"])
		#self.cookies[self.cookies["name"]] = r.cookies.get_dict()[self.cookies["name"]]
		#tokens = re.findall(self.csrf["pattern"],r.text)

