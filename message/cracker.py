from itertools import product

from message.plaintext import Plaintext

# ---------+-----------------------------------+---------------------------
# Bits  00 | ................ ................ | Control characters
# 5-6:  01 |  !"#$%&'()*+,-./ 0123456789:;<=>? | Numbers and punctuation
#       10 | @ABCDEFGHIJKLMNO PQRSTUVWXYZ[\]^_ | Uppercase letters (mostly)
#       11 | `abcdefghijklmno pqrstuvwxyz{|}~. | Lowercase letters (mostly)

#         00   01   10   11                     m1 xor m2 is a control character :
#                                                   m1, m2 of same type
#   00    00   01   10   11
#                                               m1 xor m2 is a number/punctuation character :
#   01    01   00   11   10        ----->           m1, m2 are lowercase & uppercase
#
#   10    10   11   00   01                     m1 xor m2 is a lowercase OR uppercase character :
#                                                   m1 = number/punctuation, m2 = !case(m1 xor m2)
#   11    11   10   01   00
from message.xorable import Xorable
from itertools import chain


class Cracker:
    control_characters_range = range(0, 32)
    numbers_punctuation_range = range(32, 64)
    uppercase_range = range(64, 96)
    lowercase_range = range(93, 128)
    letter_range = list(range(65, 91)) + list(range(97, 123))
    common_punctuation = list(map(ord, [' ', '.', '?', '!', ',', '(', ')', '-', ';', ':']))

    def __init__(self, ciphertexts) -> None:
        super().__init__()
        self.original_ciphertexts = ciphertexts
        self.ciphertexts = ciphertexts
        print(len(ciphertexts))
        self.ciphertexts.sort(key=lambda x: x.length, reverse=True)
        self.key_length = max([ciphertext.length for ciphertext in ciphertexts])
        self.key = [-1] * self.key_length
        self.c0 = self.ciphertexts[0]
        self.ch = self.ciphertexts[1]
        self.c1 = None
        self.hits = []
        self.c2 = None
        print(self.common_punctuation_xors)

        # print(self.letter_range)
        # print(self.common_punctuation)
        #
        # print(len(ciphertexts))


    def crack(self):
        print("crack")

        for i in range(1, len(self.ciphertexts)):
            for j in range(i, len(self.ciphertexts)):
                print(i)
                print(self.ciphertexts[i])
                self.c1 = self.ciphertexts[i]
                self.c2 = self.ciphertexts[j]
                self.hits = [False] * self.c1.length

                xored_c1c2 = self.c1.xor(self.c2)
                xored_c1c0 = self.c1.xor(self.c0)

                print
                for i,j in zip(xored_c1c2, xored_c1c2):
                    if xored_c1c2 in self.letter_range and xored_c1c0 in self.letter_range:
                        self.hits = True

                    i

                print(self.hits)




        # print(self.key)
        #
        # key_xorable = Xorable(self.key)
        #
        # for i in range(len(self.original_ciphertexts)):
        #     plaintext = key_xorable.xor(self.original_ciphertexts[i])
        #     clear = self.clear_plaintext(plaintext)
        #
        #     plaintext_xorable = Xorable(list(clear))
        #     print(plaintext_xorable.as_string())

    def clear_plaintext(self, plaintext):
        for sign in plaintext:
            if sign in range(32, 128):
                yield sign
            else:
                yield ord("_")

    def calculate_key(self, index, char):

        for punctuation in self.common_punctuation:
            if self.is_valid(punctuation, index):
                return char ^ punctuation

    def is_valid(self, guess, index):
        for ciphertext in self.ciphertexts:
            print("xor guess {}".format(ciphertext.get(index) ^ guess))
            if (ciphertext.get(index) ^ guess) not in self.letter_range + list(self.numbers_punctuation_range):
                return False
        return True

    def guess_key(self, xored_char, index):

        flipped_char = self.__flip_case__(xored_char)

        key_candidate_1 = flipped_char ^ self.c1.get(index)
        key_candidate_2 = flipped_char ^ self.c2.get(index)

        c_with_encrypted_space = self.who_has_space(xored_char, index)

        if c_with_encrypted_space is None:
            return

        print("Letter owner: {}".format(c_with_encrypted_space.get(index)))

        k = self.calculate_key(index, c_with_encrypted_space.get(index))

        if k is None:
            return

        print("Key {}, index {}".format(k, index))
        self.key[index] = k

    def who_has_space(self, xored_char, key_index):

        test_char = self.c0.get(key_index)

        print("test char {}, my char {}".format(test_char, xored_char))
        print("Index: {}, c0: {}, c1: {}, c2: {}".format(key_index, self.c0.get(key_index), self.c1.get(key_index),
                                                         self.c2.get(key_index)))

        xor1 = test_char ^ self.c1.get(key_index)
        xor2 = test_char ^ self.c2.get(key_index)

        print("xor1 {}".format(xor1))
        print("xor2 {}".format(xor2))

        if xor1 in self.letter_range:
            return self.c1

        if xor2 in self.letter_range:
            return self.c2

        #
        # if xor1 in self.numbers_punctuation_range:
        #     print("case 1")
        #     return self.c1
        #
        # if xor2 in self.numbers_punctuation_range:
        #     print("case 2")
        #     return self.c2
        #
        # if xor1 != xored_char and xor1 in self.letter_range:
        #     return self.c2
        # elif xor2 != xored_char and xor2 in self.letter_range:
        #     return self.c1
        #
        # if xor1 == xored_char:
        #     print("case 3")
        #     return self.c2
        #
        # if xor2 == xored_char:
        #     print("case 4")
        #     return self.c1

        # if xored_char in self.lowercase_range and xor1 in self.lowercase_range:
        #     print("case 5")
        #     return self.c2
        #
        # if xored_char in self.uppercase_range and xor1 in self.uppercase_range:
        #     print("case 6")
        #     return self.c2
        #
        # if xored_char in self.lowercase_range and xor2 in self.lowercase_range:
        #     print("case 7")
        #     return self.c1
        #
        # if xored_char in self.uppercase_range and xor2 in self.uppercase_range:
        #     print("case 8")
        #     return self.c1

    def __flip_case__(self, i):
        if i in self.lowercase_range:
            return i - 32
        elif i in self.uppercase_range:
            return i + 32

        raise ValueError("ASCII code {} is not a letter")
