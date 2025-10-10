
# this class iterates over all capitalized letters in a string
class CapitalLettersIterator:
    def __init__(self, text):
        self._text = text[:]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        while self._index < len(self._text):
            current_char = self._text[self._index]
            self._index += 1
            if current_char.isupper():
                return current_char
        raise StopIteration


text = 'This is a Test! Yay!'
capital_letters = CapitalLettersIterator(text)

for cletter in capital_letters:
    print(cletter)
