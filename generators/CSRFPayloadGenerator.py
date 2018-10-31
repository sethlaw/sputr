class CSRFPayloadGenerator:

    @classmethod
    def create_payload(cls, name, value):
        return "<input type=\"hidden\"  name=" + "\"" + name + "\"" + " value=" + "\"" + value + "\"" + " />\n"
