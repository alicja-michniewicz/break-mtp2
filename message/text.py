class Text:

    def __init__(self, text="") -> None:
        super().__init__()
        self.characters = list(text)
        self.length = len(text)

    def flip_case(self, i: int):
        if i >= self.length:
            pass

        c = self.characters[i]

        if 'A' <= c <= 'Z':
            self.characters[i] = c.lower()

        if 'a' <= c <= 'z':
            self.characters[i] = c.upper()

    def as_string(self):
        print(self.characters)
        return ''.join(self.characters)

    def __str__(self) -> str:
        return self.as_string()

    @classmethod
    def order_by_length(cls, first, second):
        if first.length <= second.length:
            return first, second
        else:
            return second, first
