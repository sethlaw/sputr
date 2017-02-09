#!/usr/bin/python
#####################################
# generate_payloads.py
# created: 2017-01-20
# author: seth
#####################################
import json
import sys
from testgen.sqli_test import SQLi_test

sys.dont_write_bytecode = True

def main():
	d = parse_config()
	generate_test_suite(d)



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
	print("Generated Config")


def parse_config():
	with open('config.json','r') as config:
		d = json.loads(config.read())
	return d

def generate_test_suite(config):
	for endpoint in config["endpoints"]:
		test = list(endpoint["tests"])
		if test[0] == '1':
			generate_sqli_test()
		if test[1] == '1':
			generate_xss_test()
		if test[2] == '1':
			generate_idor_test()
		if test[3] == '1':
			generate_csrf_test()

		

def generate_xss_test():
	print("Generating XSS Test")

def generate_sqli_test():
	print("Generating SQLi Test")

def generate_idor_test():
	print("Generating IDOR Test")

def generate_csrf_test():
	print("Generating CSRF Test")


if __name__ == "__main__":
	main()