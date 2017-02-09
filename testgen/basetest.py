#base class for all unit test generators
class Test():
	def __init__(self):
		print("init")
	
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
		#mock a service call
