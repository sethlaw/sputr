#!/usr/bin/python
#####################################
# generate_payloads.py
# created: 2017-01-20
# author: seth
#####################################

import os
import random
import string

class Payloads():
	
	chars_dir = os.getcwd() + "/exploit_chars"
	payloads_dir = os.getcwd() + "/payloads"

	def process_chars_dir(dir):
		dirs = os.listdir(dir)
		payloads = []
		chars = {}
		for f in dirs:
			p = os.path.join(dir,f)
			if os.path.isdir(p):
				process_chars_dir(p)
			else:
				file = open(p)
				for l in file:
					c = l.rstrip('\n')
					chars[c] = 1
		return chars		
	
	#process_chars_dir(chars_dir,"/")
	
	def generate_payloads(type):
		#type can be xss, sqli, xml
		print('Generating payload list for ' + type)
		dir = os.getcwd() + "/exploit_chars" + "/" + type
		s = string.ascii_lowercase + string.digits
		
		payloads = []
		chars = Payloads.process_chars_dir(dir)
		for c in chars:
			r = ''.join(random.sample(s,5))
			p = r + c + r
			payloads.append(p)
		return payloads