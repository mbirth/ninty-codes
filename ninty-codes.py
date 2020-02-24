#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ninty.example_codes import EXAMPLE_CODES
from functools import reduce

# https://www.reddit.com/r/SwitchHacks/comments/f7psrk/anatomy_of_an_eshop_card_code/

CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def safe2real(code: str):
    """Converts a code with unambiguous characters to the real code"""
    code = code.upper()
    code = code.replace('V', 'A')   # A might be confused with 4
    code = code.replace('W', 'E')   # E might be confused with 3
    code = code.replace('X', 'I')   # I might be confused with 1
    code = code.replace('Y', 'O')   # O might be confused with 0
    return code

def generateChecksum(base_code, base = 30):
    if len(base_code) != 15:
        raise RuntimeError("Bad argument to checksum")
    # https://www.reddit.com/r/SwitchHacks/comments/f7psrk/anatomy_of_an_eshop_card_code/fijt5d4/
    cksum = sum(int(c, base) for c in base_code) % base
    return CHARSET[cksum]

def validate(code):
    if len(code) != 16: return False
    # Make uppercase if necessary, then change X and Y back to their base 33 equivalents
    unmangled_code = safe2real(code)
    theirs = unmangled_code[15]
    code_type = get_type(code)
    base = 33 if code_type == '_A_' else 30
    mine = generateChecksum(unmangled_code[0:15], base)
    return theirs == mine

def parse(code):
    serial = None
    external_validator = None
    code_type = get_type(code)
    unmangled_code = safe2real(code)
    if code_type == 'NUM':
        serial = int(code[0:8])
        external_validator = int(code[8:])
    elif code_type == '_A_':
        serial = int(unmangled_code[1:8], 33)
        external_validator = int(unmangled_code[8:15], 33)
    elif code_type == '_B_' or code_type == '_C_':
        serial = int(unmangled_code[1:8], 30)
        external_validator = int(unmangled_code[8:15], 30)
    else:
        print(" unknown card generation '%s'" % code[0])
        return

    print(" ser#: {:010d} / Ext. validator: {:010d}".format(serial, external_validator))

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
        args = EXAMPLE_CODES
    else:
        args = sys.argv[1:]
    seen_chars = {}
    for s in args:
        code_type = get_type(s)
        if not code_type in seen_chars:
            seen_chars[code_type] = set()
        for c in s[1:]:
            seen_chars[code_type].add(c)
        if code_type != 'NUM':
            valid = validate(s)
            print('{} {}'.format(s, "☑ " if valid else "☒ "), end='')
            if not valid:
                print()
                continue
            parse(s)
        else:
            print('{} ??'.format(s), end='')
            parse(s)
    for ct, cc in seen_chars.items():
        cc = sorted(list(cc))
        print('Found characters in type {} codes: '.format(ct), end='')
        for c in CHARSET:
            if c in cc:
                print(c, end='')
            else:
                print('-', end='')
        print()
