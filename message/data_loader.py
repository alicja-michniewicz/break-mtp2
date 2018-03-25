import re

from message.xorable import Xorable


def load_from_file(filename: str):
    with open(filename) as f:
        return re.findall(r'(?:[01]{8} ?)+\n', f.read())


def decode_bytes(byte_array):
    return [text_from_bits(byte) for byte in byte_array]


def decode_byte_strings(strings):
    return [decode_bytes(strings[i].split(" ")) for i in range(len(strings))]


def text_from_bits(bits):
    n = int('0b' + bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding='utf-8', errors='surrogateescape') or '\0'

def load_ciphertexts_from_file(filename: str):
    binary_ciphertexts = load_from_file(filename)
    integer_ciphertexts = list(decode_to_ints(binary_ciphertexts))

    return [Xorable(integer_ciphertext) for integer_ciphertext in integer_ciphertexts]

def decode_to_ints(binary_ciphertexts):
    for binary_ciphertext in binary_ciphertexts:
        bytes = binary_ciphertext.split(" ")
        yield [int(byte,2) for byte in bytes]
