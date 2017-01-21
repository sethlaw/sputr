#!/usr/bin/python
#####################################
# generate_payloads.py
# created: 2017-01-20
# author: seth
#####################################

import os
import random
import string

chars_dir = os.getcwd() + "/exploit_chars"
payloads_dir = os.getcwd() + "/payloads"
DEBUG = 1
s = string.ascii_lowercase + string.digits
#s=string.lowercase+string.digits



def process_chars_dir(dir,prefix):
	dirs = os.listdir(dir)
	for f in dirs:
		p = os.path.join(dir,f)
		if os.path.isdir(dir + "/" + f):
			#print("Dir: " + dir + "/" + f)
			if not os.path.exists(payloads_dir+prefix+f):
				if DEBUG: print("Creating directory " + payloads_dir + prefix + f)
				os.mkdir(payloads_dir+prefix+f)
			#else:
			#	print("Dir exists " + payloads_dir + prefix + f)
			process_chars_dir(os.path.join(dir,f),prefix+f+"/")
		else:
			if DEBUG: print("Processing character file: " + dir + "/" + f)
			file = open(dir + "/" + f)
			out = open(payloads_dir + prefix + f, "w")
			for l in file:
				r = ''.join(random.sample(s,5))
				p = r + l.rstrip() + r
				c = l.rstrip()
				if DEBUG: print("Created payload: " + p)
				out.write(p + "\n")
			

process_chars_dir(chars_dir,"/")