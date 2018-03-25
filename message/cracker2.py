from itertools import product

import sys

from message.xorable import Xorable


class Cracker:
    control_characters_range = range(0, 32)
    numbers_punctuation_range = range(32, 64)
    uppercase_range = range(64, 96)
    lowercase_range = range(96, 128)
    common_letter_range = list(range(65, 91)) + list(range(97, 123))
    letter_range = range(64, 128)
    common_punctuation = [32, 33, 40, 41, 44, 46, 58, 59, 63]
    common_punctuation_xors = list(set(s1 ^ s2 for s1, s2 in product(common_punctuation, common_punctuation)))
    text_allowed_chars = common_punctuation + common_letter_range + [39, 45]

    def __init__(self, ciphertexts) -> None:
        super().__init__()
        self.original_ciphertexts = ciphertexts
        self.ciphertexts = ciphertexts
        self.ciphertexts.sort(key=lambda x: x.length, reverse=True)

        self.key_length = max([ciphertext.length for ciphertext in ciphertexts])

        self.key = [-1] * self.key_length

        self.c0 = self.ciphertexts[0]

        self.c1 = None
        self.hits = []
        self.c2 = None
        print(self.common_punctuation_xors)

        # print(self.letter_range)
        # print(self.common_punctuation)
        #
        # print(len(ciphertexts))

    def compare_hits(self, all_hits):
        common_hits = [1] * len(all_hits[0])

        print("compare")
        for hit in all_hits:
            print("hit")
            print(hit)
            for i in range(len(hit)):
                if not hit[i]:
                    common_hits[i] = 0

        self.hits = common_hits
        return common_hits

    def crack(self):
        for i in range(0, len(self.ciphertexts)):
            self.c1 = self.ciphertexts[i]

            self.detect_all_hits()
            # print(self.hits)
            self.detect_spaces()

        self.fix_key()
        print(self.key)
        self.decode()

    def guess(self):
        user_input = None
        while user_input is not "N":
            user_input = input("Do you want to guess a letter? Y/N ")

            if user_input is "Y":
                row = int(input("Row "))
                column = int(input("Column "))
                value = input("Value ")

                print("Row {} column {} value {}".format(int(row), int(column), value))

                key_proposition = self.ciphertexts[row].get(column) ^ ord(value)
                self.key[column] = key_proposition

                self.decode()

    def detect_all_hits(self):
        xors = self.xor_all_with(self.c1)

        # print(xors)

        all_hits = []
        for single_xor in xors:
            all_hits.append(self.single_hits(single_xor))

        self.compare_hits(all_hits)

    def xor_all_with(self, root):
        xors = []

        for c in self.ciphertexts:
            if c is not root:
                xors.append(root.xor(c))

        return xors

    def detect_spaces(self):

        print("spaces")
        print(self.hits)
        for i in range(len(self.hits)):
            self.detect_double_interpunction(i)
            self.detect_single_space(i)

    def detect_double_interpunction(self, i):
        if i >= len(self.hits) - 3:
            return

        if self.hits[i] == 0 and self.hits[i + 1] == 1 and self.hits[i + 2] == 1 and self.hits[i + 3] == 0:
            self.key[i + 2] = self.c1.get(i + 2) ^ ord(' ')
            print("DOUBLE")

    def detect_three_punctuation_marks(self, i):
        if i >= len(self.hits) - 2:
            return

        if self.hits[i] == True and self.hits[i + 1] == True and self.hits[i + 2] == True:
            self.key[i] = self.c1[i] ^ ord(' ')
            self.hits[i + 1] = False

    def detect_single_space(self, i):
        if i >= len(self.hits) - 2:
            return

        if self.hits[i] == 0 and self.hits[i + 1] == 1 and self.hits[i + 2] == 0:
            self.key[i + 1] = self.c1.get(i + 1) ^ ord(' ')

    def decode(self):
        print(self.key)

        key_xorable = Xorable(self.key)

        for i in range(len(self.original_ciphertexts)):
            plaintext = key_xorable.xor(self.original_ciphertexts[i])
            clear = self.clear_plaintext(plaintext)

            plaintext_xorable = Xorable(list(clear))
            print(plaintext_xorable.as_string())

    def clear_plaintext(self, plaintext):
        for sign in plaintext:
            if sign in range(32, 128):
                yield sign
            else:
                yield ord("_")

    def single_hits(self, single_xor):
        hits = [0] * len(single_xor)

        for i in range(len(single_xor)):
            # space xor letter
            if single_xor[i] in self.letter_range:
                hits[i] = 1
                continue

            # double spaces
            if single_xor[i] == 0:
                hits[i] = 1
                continue

            # double punctuation
            if single_xor[i] in self.common_punctuation_xors:
                hits[i] = 1
                continue

            print("{} {}".format(chr(single_xor[i]), single_xor[i]))
        return hits

        pass

    def fix_key(self):
        for i in range(self.key_length):
            if self.key[i] == -1:
                self.brute_force(i)

            if not self.check_key(i, self.key[i]):
                self.brute_force(i)

        pass

    def check_key(self, i, key):
        if i == 52:
            print("Checking key {} at position {}".format(key, i))

        for ciphertext in self.ciphertexts:
            if i == 52:
                print("Xor {}".format(ciphertext.get(i) ^ key))

            if ciphertext.get(i) ^ key not in self.text_allowed_chars:
                if i == 52:
                    print("Xor not in readable")

                return False

        print("found key")
        return True

    def brute_force(self, i):
        for potential_key in range(0, 256):
            if self.check_key(i, potential_key):
                self.key[i] = potential_key
                print("found key")
                return
