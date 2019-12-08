import textwrap
import conversion
import permutations
import misc


def encrypt(text, key):
    binary_text = misc.text_to_bits(text)
    binary_text = textwrap.wrap(binary_text, 64)

    last_text_part = binary_text[len(binary_text) - 1]
    binary_text[len(binary_text) - 1] = last_text_part + ''.zfill(64-len(last_text_part))

    subkeys = conversion.primary_key_to_subkeys(key)

    for part_num, part in enumerate(binary_text):
        part = permutations.permutation(part, "initial")
        lpt, rpt = part[:int(len(part) / 2)], part[int(len(part) / 2):]
        for i in range(16):
            lpt, rpt = rpt, misc.binary_addition(lpt, function(rpt, subkeys[0]), 32)
        binary_text[part_num] = permutations.permutation(rpt + lpt, "inverse")
    return ''.join(binary_text)


def function(rpt, subkey):
    rpt = permutations.permutation(rpt, "expansion")
    rpt = misc.XOR(rpt, subkey)
    rpt = permutations.sBox_permutation(rpt)
    rpt = permutations.permutation(rpt, "pBox")
    return rpt
