import unittest

from message.xorable import Xorable


class TestCiphertext(unittest.TestCase):

    def test_xor_givenCiphertexts_correctXorOnPositionX(self):
        text_1 = Xorable([1, 2, 3])
        text_2 = Xorable([1, 2, 1])

        self.assertEqual(text_1.xor(text_2)[2], 2)

    def test_xor_givenCiphertexts_correctLength(self):
        text_1 = Xorable([1, 2, 3, 4])
        text_2 = Xorable([1, 2, 1])

        xor = text_1.xor(text_2)

        self.assertEqual(len(xor), 3)


if __name__ == '__main__':
    unittest.main()
