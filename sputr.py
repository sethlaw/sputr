#!/usr/bin/python
#####################################
# generate_payloads.py
# created: 2017-01-20
# author: seth
#####################################
import json
import sys
import argparse
import requests
import pprint
from services.token_service import TokenService 
from services.poc_service import POCService 
from tests.csrf_test import CSRFTest
from tests.xss_test import XSSTest
from tests.sqli_test import SQLiTest
from tests.access_control_test import AccessControlTest
from generators.payload_generator import Payloads

sys.dont_write_bytecode = True

def main():
	parser = argparse.ArgumentParser(description='sputr.py')
	parser.add_argument('--config',dest='config',default='config.json',help='config file (default: config.json)')
	parser.add_argument('--test',action='store_true', help='start tests')
	parser.add_argument('--generate',action='store_true', help='generate config file for app')
	parser.add_argument('--apptype',dest='apptype',help='application type for config generation (django|flask|spring|dotnet)')
	parser.add_argument('--appdir',dest='appdir',help='application directory for config generation')
	parser.add_argument('--output',dest='output',default='config.json',help='file to output config file to')
	parser.add_argument('--testcsrf',action='store_true', help='test csrf from initial dev')
	
	args = parser.parse_args()
	
	pp = pprint.PrettyPrinter(indent=4)
	
	if args.testcsrf: 
		session = requests.Session()
		creds = {
			"username":"username",
			"password":"password"
			}
		payloads =	{
			"username":"admin",
			"password":"password",
			"email":"example@email.com"
			}
		url = "http://localhost:1234/api/create"
		poc = POCService(payloads)
		poc.writeToFile(poc.csrf_poc(url))
		with requests.Session() as s:
			res1 = s.post("http://localhost:1234/api/login",data=creds) # Authenticate
			res2 = s.post(url,data=payloads)
			if res1.status_code == res2.status_code:
				passed = False
				print("TEST FAILED")
		
	elif args.test:
		c = parse_config(args.config)
		#pp.pprint(c)
		creds = c['creds']
		domain = c['domain']
		csrf = c['csrf']
		for ep in c['endpoints']:
			tests = list(ep['tests'])
			if tests[0] == '1':
				print('running sqli tests')
				sqli_payloads = Payloads.generate_payloads('injection/sql')
				sqli = SQLiTest(ep,domain,creds,csrf,sqli_payloads,DEBUG=False)
				sqli.test()
			if tests[1] == '1':
				print('running xss tests')
				xss_payloads = Payloads.generate_payloads('xss')
				xss = XSSTest(ep,domain,creds,csrf,xss_payloads,DEBUG=False)
				xss.test()
			if tests[2] == '1':
				print('running IDOR tests')
			if tests[3] == '1':
				#Do CSRF Test
				print('running CSRF tests')
			if tests[4] == '1':
				print('running access control tests')
				ac = AccessControlTest(ep,domain,creds,csrf,[],DEBUG=False)
				ac.test()
	elif args.generate:
		print('generating config from ' + args.appdir + ' as a ' + args.apptype + ' application to ' + args.output)
		generate_config(args.appdir,args.apptype,args.output)
	else:
		parser.print_help()
	return 0

def generate_config(appdir,apptype,output):
	#TEST
	config = {}
	config['token'] = {}
	config['token']['name']= 'cookie_name'
	config['token']['value']= 'cookie_value'
	config['creds'] = {}
	config['creds']['username'] = {}
	config['creds']['username']['name']= 'username'
	config['creds']['username']['value']= 'testuser'
	config['creds']['password'] = {}
	config['creds']['password']['name']= 'password'
	config['creds']['password']['password']= 'temppass'
	config['csrf'] = {}
	config['csrf']['pattern'] = '^regexpattern$'
	config['csrf']['name'] = 'csrftokenname'
	config['domain'] = {}
	config['domain']['host'] = 'localhost:8000'
	config['domain']['protocol'] = 'http://'
	config['domain']['login_url'] = 'http://localhost:8000/taskManager/login'
	config['domain']['auth_url'] = 'http://localhost:8000/taskManager/dashboard'
	config['endpoints'] = []
	ep = {}
	ep['path'] = '/'
	ep['method'] = 'GET'
	ep['auth'] = 0
	ep['params'] = {}
	ep['tests'] = "11111"
	config['endpoints'].append(ep)
	if apptype == 'django':
		print('adding django endpoints')
		#TODO django parsing
	elif apptype == 'java':
		print('adding java spring endpoints')
		#TODO java spring parsing
	elif apptype == 'dotnet':
		print('adding dotnet mvc endpoints')
		#TODO dotnet mvc parsing
	elif apptype == 'flask':
		print('adding flask endpoints')
		#TODO flask parsing
	with open(output,'w') as f:
		json.dump(config,f,indent=4)



def parse_config(f):
	with open(f,'r') as config:
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