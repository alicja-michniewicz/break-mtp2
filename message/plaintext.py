from message.text import Text


class Plaintext(Text):

    def __init__(self, length: int) -> None:
        super().__init__()
        self.characters = [None] * length

    def guess(self, c: str, i: int):
        if i >= len(self.characters):
            pass

        if len(c) != 1:
            pass

        self.characters[i] = c


