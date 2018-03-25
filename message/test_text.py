import unittest

from message.text import Text


class TestText(unittest.TestCase):

    def test_givenText_correctLength(self):
        text = Text(text="abcdef")
        self.assertEqual(text.length, 6)

    def test_givenText_flippedCaseLowerToUpper(self):
        text = Text(text="abcdef")
        text.flip_case(3)
        self.assertEqual(text.characters[3], 'D')

    def test_givenText_flippedCaseUpperToLower(self):
        text = Text(text="ABCDEF")
        text.flip_case(3)
        self.assertEqual(text.characters[3], 'd')

    def test_givenText_specialCharacterNotFlipped(self):
        text = Text(text="::::::")
        text.flip_case(3)
        self.assertEqual(text.characters[3], ':')

    def test_givenText_correctString(self):
        text = Text(text="abcdef")
        self.assertEqual("abcdef", text.as_string())

if __name__ == '__main__':
    unittest.main()
