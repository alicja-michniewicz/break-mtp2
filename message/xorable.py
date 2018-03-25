from message.text import Text


class Xorable:
    def __init__(self, characters_int: [int]) -> None:
        self.characters = characters_int
        self.length = len(characters_int)

    def _xor_(self, other, i: int):
        # print("{} xor {} == {}".format(self.characters[i], other.characters[i], self.characters[i] ^ other.characters[i]))
        return self.characters[i] ^ other.characters[i]

    def xor(self, other):
        shorter, longer = Text.order_by_length(self, other)

        return [self._xor_(other, i) for i in range(shorter.length)]

    def as_string(self):
        return ''.join(chr(character) for character in self.characters)

    def get(self, i):

        if i >= self.length:
            return -1

        return self.characters[i]

    def __str__(self) -> str:
        return ''.join(chr(character) for character in self.characters)
