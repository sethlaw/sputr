#!/usr/bin/python
#####################################
# generate_payloads.py
# created: 2017-01-20
# author: seth
#####################################
import json

def main():
	parse_config()



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
	print(d)
	generate_test_suite(d)


def generate_test_suite(config):
	#Generate the Test Suite based off of the Config File
	print("Generating Security Unit Tests")






if __name__ == "__main__":
	main()