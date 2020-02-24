#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import product
from ninty.codes import safe2real, real2safe, generate_checksum, validate, get_type, CHARSET

args = None
if len(sys.argv) == 1:
    print("Syntax: {} [A0...]".format(sys.argv[0]))
    print("        replace unidentified characters with *")
    sys.exit(1)

code = sys.argv[1]
if len(code) != 16:
    print("Code must be exactly 16 characters long.")
    sys.exit(2)

code_type = get_type(code)
if not code_type in ['_A_', '_B_', '_C_']:
    print("Code must be starting with 'A', 'B' or 'C'!")
    sys.exit(3)

base = 30
if code_type == '_A_':
    base = 33

real_code = safe2real(code)

print("Actual code: {}".format(real_code))

unknowns = 0
for c in real_code:
    if c == '*':
        unknowns += 1

if unknowns == 0:
    print("No unknown digits. Nothing to do.")
    sys.exit(4)

print("{} unknown digits. {} combinations.".format(unknowns, len(CHARSET)**unknowns))

print("Valid codes:")

repstring = real_code.replace("*", "{}")
for p in product(CHARSET[:base], repeat=unknowns):
    test_code = repstring.format(*p)
    isvalid = validate(test_code)
    if isvalid:
        print(real2safe(test_code))
