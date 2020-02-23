#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
from itertools import product

CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXY'

def safe2real(code: str):
    """Converts a code with unambiguous characters to the real code"""
    code = code.upper()
    code = code.replace('V', 'A')   # A might be confused with 4
    code = code.replace('W', 'E')   # E might be confused with 3
    code = code.replace('X', 'I')   # I might be confused with 1
    code = code.replace('Y', 'O')   # O might be confused with 0
    return code

def generateChecksum(base_code):
    if len(base_code) != 15:
        raise RuntimeError("Bad argument to checksum")
    # Mystery/bug: Why is this ord('7') in particular? 55, 0o55 and 0x55 are all unrelated to anything in base 33. The check looks like it's trying to do c - 'A', but does the weirdest thing instead.
    cksum = reduce(lambda cksum, c: (cksum + (ord(c) - ord('0') if ord(c) <= ord('9') else ord(c) - ord('7'))) % 33, base_code, 0)
    return CHARSET[cksum]

def validate(code):
    if len(code) != 16: return False
    theirs = code[15]
    mine = generateChecksum(code[0:15])
    return (theirs == mine)

def get_type(code: str) -> str:
    if code[0].isnumeric():
        return 'NUM'
    elif code[0] == 'A':
        return '_A_'
    elif code[0] == 'B':
        return '_B_'
    elif code[0] == 'C':
        return '_C_'
    else:
        return 'UNK'

if __name__ == '__main__':
    import sys
    args = None
    if len(sys.argv) == 1:
        print("Syntax: {} [A0...]".format(sys.argv[0]))
        print("        replace unidentified characters with *")
        sys.exit(1)

    code = sys.argv[1]
    if len(code) != 16:
        print("Code must be exactly 16 characters long.")
        sys.exit(2)

    if get_type(code) != '_A_':
        print("Code must be starting with 'A'!")
        sys.exit(3)

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
    for p in product(CHARSET, repeat=unknowns):
        test_code = repstring.format(*p)
        isvalid = validate(test_code)
        if isvalid:
            print(test_code)
