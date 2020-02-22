From: https://www.reddit.com/r/SwitchHacks/comments/f7psrk/anatomy_of_an_eshop_card_code/

Quite some years ago, [an effort has been made to look into how eShop codes worked](https://www.reddit.com/r/3dshacks/comments/5i1rhc/eshop_codes_out_of_curiosity/), but nothing really came from it. In the meantime, I've taken to actually analyzing the results, and we now know:

- There are (at least) three generations of eShop codes.
- How to decode the 'A' generation.
- How to validate the 'A' generation.

I'd like to thank /u/teseting in particular because [they noticed that there is a split between the first eight characters and the second eight characters](https://www.reddit.com/r/3dshacks/comments/5i1rhc/eshop_codes_out_of_curiosity/db5zkw2/), greatly accelerating my research on this.

# Generations of codes

There are at least three "generations" of eShop codes. Each generation has its own format and different kinds of validation.

The **numeric generation** is the first generation of eShop codes. Each code consists of two eight-character halves. The first half is a monotonically increasing serial number. The second half is a high-entropy value. It is speculated that this second half actually be encrypted with a 64-bit block cipher (DES?); I've tentatively dubbed it the *external validator* because if there is validation to be had, it's external to the code itself. Codes for the numeric generation could be found in the wild around 2011.

The **'A' generation** is the second generation of eShop codes. These codes have been in the wild since at least 2014, likely somewhat earlier. It is called the 'A' generation because the first character for these codes is always 'A'. It consists of four parts: The leading generation identifier 'A', a seven-character serial number in base 33XY encoding, a seven-character external validator in base 33XY encoding and a checksum in base 33XY encoding. Base 33XY is regular base 33 encoding (0123456789ABCDEFGHIJKLMNOPQRSTUVW), but the vowels 'O' and 'I' are replaced with the characters 'X' and 'Y', respectively.

With some elbow grease, good guesses and trying out some constants, it has been possible to determine the checksum for the 'A' generation codes (pseudocode follows). It's a simple additive checksum that *looks* like it was meant to add the base 33 value of characters, but then messed up handling the alphabetic characters. Sample code can be found at the bottom of this post.

The **'B' generation** is the current generation of eShop codes and the one that has been going since about 2015 or 2016. Little is known other than it apparently still using the base 33XY encoding. However, the checksum algorithm for the 'A' generation no longer works.

# Additional speculation

As far as I can tell, considering the somewhat small sample size, there are no predefined numeric ranges for eShop codes depending on purpose. Money and all kinds of contents are just generated with an increasing serial number.

Even if codes have a valid checksum, they seem to be rejected by the system, so there's some kind of additional validation still taking place on the backend (maybe a check against a database). Because of the 64-bit-ish external validator, brute forcing codes is similarly infeasible. Perhaps 'B' generation codes have done away with the checksum; if so, then the fact that they still need to check the external validator is likely the cause for dropping it.
