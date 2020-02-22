#!/usr/bin/env python2

def generateChecksum(base_code):
    if len(base_code) != 15:
        raise RuntimeError("Bad argument to checksum")
    # Mystery/bug: Why is this ord('7') in particular? 55, 0o55 and 0x55 are all unrelated to anything in base 33. The check looks like it's trying to do c - 'A', but does the weirdest thing instead.
    cksum = reduce(lambda cksum, c: (cksum + (ord(c) - ord('0') if ord(c) <= ord('9') else ord(c) - ord('7'))) % 33, base_code, 0)
    return '0123456789ABCDEFGHIJKLMNOPQRSTUVW'[cksum]

def validate(code):
    if len(code) != 16: return False
    # Make uppercase if necessary, then change X and Y back to their base 33 equivalents
    unmangled_code = code.upper().replace('X', 'I').replace('Y', 'O')
    theirs = unmangled_code[15]
    mine = generateChecksum(unmangled_code[0:15])
    return theirs == mine

def parse(code):
    serial = None
    external_validator = None
    unmangled_code = code.upper().replace('X', 'I').replace('Y', 'O')
    if code[0].decode('ASCII').isnumeric():
        serial = long(code[0:8])
        external_validator = long(code[8:])
    elif code[0] == 'A':
        serial = long(unmangled_code[1:8], 33)
        external_validator = long(unmangled_code[8:15], 33)
    elif code[0] == 'B':
        serial = long(unmangled_code[1:8], 33)
        external_validator = long(unmangled_code[8:15], 33)
        print "warning: Format for 'B' generation speculative"
    else:
        print "unknown card generation '%s'" % code[0]
        return

    print "Serial number:      {0:010d}".format(serial)
    print "External validator: {0:010d}".format(external_validator)

if __name__ == '__main__':
    import sys
    # taken from the interwebs, none of these are new
    predef = (
            '5753437561933377',
            '5753437675070492',
            'A03RL0KB2XHHRRBD',
            'A03RL0KC22JL2MEA',
            'A03RL0KD0UXF49FK',
            'A03RL0KE1X8GGMS6',
            'A0796BH71Q1DSSYN',
            'B0GLFY1H1QR5GGDT',
            'B0K777732YWS7XVF',
            )
    args = None
    if len(sys.argv) == 1:
        args = predef
    else:
        args = sys.argv[1:]
    for s in args:
        if s[0] == 'A':
            valid = validate(s)
            print '%s: %s' % (s, "ok" if valid else "bad")
            if not valid: continue
            parse(s)
        else:
            print s
            parse(s)
        print ""
