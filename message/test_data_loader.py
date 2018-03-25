import unittest
from message.data_loader import load_from_file, decode_byte_strings, decode_bytes


class TestDataLoader(unittest.TestCase):

    def test_loadCiphertexts(self):
        results = load_from_file("test_file.txt", 0)

        print(results)
        self.assertEqual(2, len(results))

    def test_decodeBytes(self):
        # char a b
        texts = decode_bytes(['01100001', '01100010'])
        print(texts)

        self.assertEqual(texts[0], 'a')
        self.assertEqual(texts[1], 'b')

    def test_decodeStrings(self):
        results = load_from_file("test_file.txt", 0)

        print(results[0])
        print(results[1])
        texts = decode_byte_strings(results)
        print(texts)


if __name__ == '__main__':
    unittest.main()
