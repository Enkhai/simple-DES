import binascii


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def hex_to_bits(text):
    bits = bin(int(text, 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def binary_addition(value1, value2, num_of_bits):
    bits = bin(int(value1, 2) + int(value2, 2))[2:]
    return bits.zfill(num_of_bits)[-num_of_bits:]


def XOR(value1, value2):
    bits = bin(int(value1, 2) ^ int(value2, 2))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def left_shift(text, d):
    Lfirst = text[0:d]
    Lsecond = text[d:]

    return Lsecond + Lfirst
