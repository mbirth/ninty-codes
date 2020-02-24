#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ninty.codes import CHARSET, safe2real, get_type, parse, validate
from ninty.example_codes import EXAMPLE_CODES
from functools import reduce

# https://www.reddit.com/r/SwitchHacks/comments/f7psrk/anatomy_of_an_eshop_card_code/

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
