
class CSRFPayloadGenerator():

	def create_payload(self,name,value):
		return "<input type=\"hidden\"  name="+"\""+name+"\""+" value="+"\""+value+"\""+" />\n"

	