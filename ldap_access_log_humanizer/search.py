import re

# A class to parse and better understand SRCH strings


class Search:
    def __init__(self, raw_string):
        self.raw_string = raw_string

    def verb(self):
        tokenized_string = self.raw_string.split(" ")

        # Check to see if we got a full (verb included) or partial string
        if tokenized_string[0].isupper():
            return tokenized_string[0]

        return ''

    def rest(self):
        tokenized_string = self.raw_string.split(" ")

        if len(tokenized_string) > 1:
            return " ".join(tokenized_string[1:])

        return ''

    def append(self, raw_string):
        tokenized_string = raw_string.split(" ")

        if len(tokenized_string) > 1:
            self.raw_string += " "
            self.raw_string += " ".join(tokenized_string[1:])
