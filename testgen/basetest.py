#base class for all unit test generators
class Test():
	def __init__(self):
		print("init")
	
	def get_payloads(self):
		print("payloads")
		#make a call to "generate_payloads.py" and get the appropriate payloads
	def setUp(self):
		#do setup

	def tearDown(self):
		#do tear down
	
	def mockService(self):
		#mock a service call