#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce

# https://www.reddit.com/r/SwitchHacks/comments/f7psrk/anatomy_of_an_eshop_card_code/

# taken from the interwebs, none of these are new
EXAMPLE_CODES = [
    '5753437561933377',
    '5753437675070492',

    'A039XJDX0WMEHG6W',
    'A03RL0KB2XHHRRBD',
    'A03RL0KC22JL2MEA',
    'A03RL0KD0UXF49FK',
    'A03RL0KE1X8GGMS6',
    'A05A259G2H2PJL5G',
    'A0693YFS0BPM6K2G',
    'A0796BH71Q1DSSYN',

    'B0GLFY1H1QR5GGDT',
    'B0K777732YWS7XVF',
    'B0QFT5QX0F2XMF3Q',
    'B0TTY433034MJ8FY',
    'B14WC53G32Y9VWVX',
    'B14CP5QN168XKTXR',
    'B14CP5QY1236N081',
    'B14CP5QP5CB1XY44',
    'B14CP5QQ311FQ5FQ',
    'B14CP5QR4Y7BG4QN',
    'B14CP5QS1X46M2L6',
    'B14CP5QT2S17K53T',
    'B14D8WQ610Q2S26S',
    'B14D8WQ7113VV6V4',
    'B14D8WQ834BFNP0G',
    'B14D8WQV3Q41N3KH',
    'B14D8WQB45PJ1M7L',

    'C00V1HK6KC0VMDLW',
    'C00V1HK7N1WF5SYR',
    'C00V1HK8PF42N06N',
    'C00V1HK90VSR0PGP',
    'C00V1HKBL941HH9T',
    'C00V1HKCJFNTF1QK',
    'C00V1HKDRW7VD14T',
    'C00V1HKFB2XP76V4',
    'C048GTST9QGLPCSY',
    'C049GTT0V2K86RKC',
    'C049GTT1QTLK1H26',
    'C049GTT277GG78L3',
    'C049GTT302810G4D',
    'C049GTT44SLTW4HV',
    'C049GTT55RYWV004',
    'C049GTT6V4S1V5M5',
    'C01DHQVVS3THVW6G',
    'C01WB9K31B1H3K03',
    'C01WRRQKCJ6YXFM3',
    'C080M7Y73KC7B37N',
    'C080M7Y8JGY35R0P',
    'C080M7Y9YWPX531M',
    'C080M7YV4MM8XG81',
    'C080M7YB7M3V2XRN',
    'C080M7YCDBS7Y13M',
    'C080M7YD74CPT83Y',
    'C080M7YW8XLRMTXK',
]

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
    return '0123456789ABCDEFGHIJKLMNOPQRSTUVW'[cksum]

def validate(code):
    if len(code) != 16: return False
    # Make uppercase if necessary, then change X and Y back to their base 33 equivalents
    unmangled_code = safe2real(code)
    theirs = unmangled_code[15]
    mine = generateChecksum(unmangled_code[0:15])
    return theirs == mine

def parse(code):
    serial = None
    external_validator = None
    unmangled_code = safe2real(code)
    if code[0].isnumeric():
        serial = int(code[0:8])
        external_validator = int(code[8:])
    elif code[0] == 'A':
        serial = int(unmangled_code[1:8], 33)
        external_validator = int(unmangled_code[8:15], 33)
    elif code[0] == 'B' or code[0] == 'C':
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
        if code_type == '_A_':
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
        print('Found characters in type {} codes: {}'.format(ct, "".join(cc)))
