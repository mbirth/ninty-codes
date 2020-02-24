#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce

# https://www.reddit.com/r/SwitchHacks/comments/f7psrk/anatomy_of_an_eshop_card_code/

# taken from the interwebs, none of these are new
EXAMPLE_CODES = [
    '4237082951213129',   # https://cr-cs.tumblr.com/post/153860583013/3ds-store-3ds-redeem-codes
    '5753437561933377',
    '5753437675070492',

    'A0387RMN33YJNGMC',   # https://cr-cs.tumblr.com/post/155573566497/cheap-eshop-codes-3ds-prepaid-card-code-generator-online
    'A039XJDX0WMEHG6W',
    'A03RL0KB2XHHRRBD',
    'A03RL0KC22JL2MEA',
    'A03RL0KD0UXF49FK',
    'A03RL0KE1X8GGMS6',
    'A05A259G2H2PJL5G',
    'A0693YFS0BPM6K2G',
#     'A071WNTC1BPR5EVU',   # https://www.nintendolife.com/news/2015/01/rumour_code_name_steam_demo_to_be_distributed_via_gamestop_stores
    'A0775H3G1MYCJW1Q',   # https://www.youtube.com/watch?v=RMsuHPbI04Y
    'A0796BH71Q1DSSYN',
    'A07K7E3702LYF1NM',   # https://www.youtube.com/watch?v=tIEnTXxSM98

    'B0GLFY1H1QR5GGDT',
    'B0K777732YWS7XVF',
    'B0QFT5QX0F2XNF3Q',   # https://www.koopatv.org/2018/07/nintendo-increase-eshop-card-font-size.html
    'B0S0W8RT3QBSRHK9',
    'B0TTY433034MJ8FY',
    'B14WC53G32Y9VWVX',
    'B14BNFY60LBD7KTG',
    'B14BNFY72J7S1T57',
    'B14BNFY8588M6FS9',
    'B14BNFY9464NHGPD',
    'B14BNFYV3F8WCLTL',
    'B14BNFYB3YDKY4Q4',
    'B14CCRDB5P74VCNR',   # https://www.reddit.com/r/splatoon/comments/a4pxmz/splatoon_codes_for_free_bought_the_family/
    'B14CCRDC0J4BRJ7T',
    'B14CCRDD4X8L97BL',
    'B14CCRDW2496B1MT',
    'B14CCRDF30RTDK3V',
    'B14CCRDG14TH9VG2',
    'B14CCRDH382RJPPQ',
    'B14CP5QN168XKTXR',
    'B14CP5QY1236N081',
    'B14CP5QP5CB1XY44',
    'B14CP5QQ311FQ5FQ',
    'B14CP5QR4Y7BG4QN',
    'B14CP5QS1X46M2L6',
    'B14CP5QT2S17K53T',
    'B14D8WQ610Q2S26S',   # https://www.reddit.com/r/splatoon/comments/9lchtb/got_the_group_online_package_but_only_two_other/
    'B14D8WQ7113VV5V4',
    'B14D8WQ834BFNP0G',
    'B14D8WQV3Q41N3KH',
    'B14D8WQB45PJ1M7L',
    'B14DGMW12MFCV33T',   # https://www.reddit.com/r/Splatoon_2/comments/ee5mhm/splatoon_2_jersey_and_shoes_codes_up_for_grabs/

    'C00V1HK6KC0VMDLW',   # https://www.reddit.com/r/splatoon/comments/ejepc2/hi_all_just_signed_up_for_the_nintendo_family/
    'C00V1HK7N1WF5SYR',
    'C00V1HK8PF42N06N',
    'C00V1HK90VSR0PGP',
    'C00V1HKBL941HH9T',
    'C00V1HKCJFNTF1QK',
    'C00V1HKDRW7VD14T',
    'C00V1HKFB2XP76V4',
    'C01DHQVVS3THVW6G',
    'C01DX9D6H4B5FS46',   # https://www.reddit.com/r/Switch/comments/cvm001/europe_splatoon_2_gear_download_code/
    'C01WB9K31B1H3K03',
    'C01WRRQKCJ6YXFM3',
    'C049GTST9QGLPCSY',   # https://www.reddit.com/r/splatoon/comments/ecc1u4/i_dont_play_splatoon_so_i_thought_i_would_gift/
    'C049GTT0V2K86RKC',
    'C049GTT1QTLK1H26',
    'C049GTT277GG78L3',
    'C049GTT302810G4D',
    'C049GTT44SLTW4HV',
    'C049GTT55RYWV004',
    'C049GTT6V4S1V5M5',
    'C049K4B12TSQB8L6',   # https://www.reddit.com/r/Splatoon_2/comments/ee5mhm/splatoon_2_jersey_and_shoes_codes_up_for_grabs/
    'C049K4B2XCRM6RD7',
    'C049K4B3S5YSCP49',
    'C049K4B4JK5LB6LH',
    'C049K4B51R1V17KC',
    'C049K4B6V37X301X',
    'C049K4B7PPP386JS',
    'C049MJJDSJHYT4WN',   # https://www.reddit.com/r/splatoon/comments/eyetsx/splatoon_2_codes/
    'C049MJJWDCMSF30C',
    'C049MJJFG50675D2',
    'C049MJJG0PFXR3HQ',
    'C049MJJHT6RTH6CX',
    'C049MJJX1YBTY02W',
    'C049MJJJW85MWP2W',
    'C04BK55WHPWT517J',   # https://www.reddit.com/r/splatoon/comments/eyetsx/splatoon_2_codes/
    'C07XVGFBSM0VLSJ7',   # https://www.reddit.com/r/splatoon/comments/f69b5z/bonus_gear_code_splatoon_2/
    'C080M7Y73KC7B37N',   # https://www.reddit.com/r/splatoon/comments/f0uyur/nintendo_gave_me_some_codes_for_in_game_items_but/
    'C080M7Y8JGY35R0P',
    'C080M7Y9YWPX531M',
    'C080M7YV4MM8XG81',
    'C080M7YB7M3V2XRN',
    'C080M7YCDBS7Y13M',
    'C080M7YD74CPT83Y',
    'C080M7YW8XLRMTXK',
]

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
