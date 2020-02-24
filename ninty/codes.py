#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://www.reddit.com/r/SwitchHacks/comments/f7psrk/anatomy_of_an_eshop_card_code/

CHARSET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def safe2real(code: str) -> str:
    """Converts a code with unambiguous characters to the real code"""
    code = code.upper()
    code_first = code[0]
    if code_first != 'A':
        code = code.replace('V', 'A')   # A might be confused with 4
        code = code.replace('W', 'E')   # E might be confused with 3
    code = code.replace('X', 'I')   # I might be confused with 1
    code = code.replace('Y', 'O')   # O might be confused with 0
    return code

def real2safe(code: str) -> str:
    """Converts an actual code to a representation with unambiguous characters"""
    code_first = code[0]
    code = code.upper()
    if code_first != 'A':
        code = code.replace('A', 'V')   # A might be confused with 4
        code = code.replace('E', 'W')   # E might be confused with 3
    code = code.replace('I', 'X')   # I might be confused with 1
    code = code.replace('O', 'Y')   # O might be confused with 0
    code = code_first + code[1:]
    return code

def generate_checksum(base_code, base = 30):
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
    mine = generate_checksum(unmangled_code[0:15], base)
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
