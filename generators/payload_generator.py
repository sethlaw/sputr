#!/usr/bin/python
#####################################
# payload_generator.py
# created: 2017-01-20
# author: seth
#####################################

import os
import random
import string


class Payloads:
    chars_dir = os.getcwd() + "/exploit_chars"
    payloads_dir = os.getcwd() + "/payloads"

    @classmethod
    def process_chars_dir(cls, directory):
        dirs = os.listdir(directory)
        chars = {}
        for f in dirs:
            p = os.path.join(directory, f)
            if os.path.isdir(p):
                Payloads.process_chars_dir(p)
            else:
                file = open(p)
                for l in file:
                    c = l.rstrip('\n')
                    chars[c] = 1
        return chars

    @classmethod
    def generate_payloads(cls, attack_type, debug=False):
        # type can be xss, sqli, xml
        if debug:
            print('Generating payload list for ' + attack_type)
        directory = os.getcwd() + "/exploit_chars" + "/" + attack_type
        s = string.ascii_lowercase + string.digits

        payloads = []
        chars = Payloads.process_chars_dir(directory)
        for c in chars:
            r = ''.join(random.sample(s, 5))
            p = r + c + r
            payloads.append(p)
        return payloads
