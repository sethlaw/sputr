from .basetest import Test

class CSRF_test(Test):

	def execute(self):
		#print(self.url)
		#print(self.config["params"])
		#print(self.cookies)
		r = self.post(self.url,self.config["params"],self.cookies)
		#print(r)
		#print("*****")
		#print(self.url)
		#print(self.config["params"])	
		#print(self.token)''
	