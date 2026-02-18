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
    def load_full_payloads(cls, attack_type, debug=False):
        """Load complete fuzz strings from payload files (one per line)."""
        directory = os.path.join(os.getcwd(), "payloads", attack_type)
        if not os.path.isdir(directory):
            if debug:
                print('No payload directory found for ' + attack_type)
            return []
        payloads = []
        for root, dirs, files in os.walk(directory):
            for fname in files:
                fpath = os.path.join(root, fname)
                with open(fpath) as f:
                    for line in f:
                        line = line.rstrip('\n')
                        if line:
                            payloads.append(line)
        return payloads

    @classmethod
    def generate_payloads(cls, attack_type, mode='chars', debug=False):
        """Generate payloads for a given attack type.

        mode='chars': Original behavior - reads single chars from exploit_chars/
                      and wraps each in random strings (random5 + char + random5).
        mode='full':  Loads complete fuzz strings from payloads/{attack_type}/
                      files (one per line). No wrapping.
        mode='both':  Union of both modes.
        """
        payloads = []

        if mode in ('chars', 'both'):
            if debug:
                print('Generating char payload list for ' + attack_type)
            directory = os.path.join(os.getcwd(), "exploit_chars", attack_type)
            if os.path.isdir(directory):
                s = string.ascii_lowercase + string.digits
                chars = Payloads.process_chars_dir(directory)
                for c in chars:
                    r = ''.join(random.sample(s, 5))
                    p = r + c + r
                    payloads.append(p)

        if mode in ('full', 'both'):
            if debug:
                print('Loading full payload list for ' + attack_type)
            full = Payloads.load_full_payloads(attack_type, debug=debug)
            payloads.extend(full)

        return payloads
