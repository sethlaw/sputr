#!/usr/bin/python
#####################################
# generate_payloads.py
# created: 2017-01-20
# author: seth
#####################################
import json
import sys
from services.Token import TokenGenerationService 
from testgen.csrf_test import CSRF_test

sys.dont_write_bytecode = True

def main():
	config = parse_config()
	token_service = TokenGenerationService(config)
	token_service.getCSRFToken()
	
	


def usage():
	print("Usage instructions <here>")

def generate_config():
	#TEST
	config = {}
	config['authkey'] = 'bananas'
	config['/v1/api/dashboard'] = 111100
	config_json = json.dumps(config)
	with open('config.json','w') as f:
		json.dump(config_json,f)



def parse_config():
	with open('config.json','r') as config:
		d = json.loads(config.read())
	return d

def generate_test_suite(config):
	for endpoint in config["endpoints"]:
		test = list(endpoint["tests"])
		url = config["domain"]["protocol"]+config["domain"]["host"]+endpoint["path"]
		token = config["token"]
		if test[0] == '1':
			generate_sqli_test()
		if test[1] == '1':
			generate_xss_test()
		if test[2] == '1':
			generate_idor_test()
		if test[3] == '1':
			generate_csrf_test(url,endpoint,token)

	
def generate_sqli_test(config):
	sqli_test = SQLi_test(config)
	print("Generating SQLi Test")

def generate_xss_test(config):
	print("Generating XSS Test")

def generate_idor_test(config):
	print("Generating IDOR Test")

def generate_csrf_test(url,config,token):
	csrf_test = CSRF_test(url,config,token)
	csrf_test.execute()
	


if __name__ == "__main__":
	main()