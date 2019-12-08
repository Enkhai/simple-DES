import misc
import permutations


def primary_key_to_subkeys(key):
    subkeys = []

    binary_prim_key = misc.hex_to_bits(key)
    binary_prim_key = ''.join([binary_prim_key[i:i + 7] for i in range(0, len(binary_prim_key), 8)])

    left_part, right_part = binary_prim_key[:int(len(binary_prim_key) / 2)], binary_prim_key[
                                                                             int(len(binary_prim_key) / 2):]
    for i in range(16):
        if i == 0 \
                or i == 1 \
                or i == 8 \
                or i == 15:
            left_part = misc.left_shift(left_part, 1)
            right_part = misc.left_shift(right_part, 1)
        else:
            left_part = misc.left_shift(left_part, 2)
            right_part = misc.left_shift(right_part, 2)
        subkeys.append(permutations.permutation(left_part + right_part, "compression"))
    return subkeys
