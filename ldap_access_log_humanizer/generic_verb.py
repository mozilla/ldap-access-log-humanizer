import re

# A class to parse and better understand BIND strings


class GenericVerb:
    def __init__(self, raw_string):
        self.raw_string = raw_string

    def dict(self):
        return {
            "verb": self.verb(),
            "rest": self.rest(),
        }

    def verb(self):
        tokenized_verb_string = self.raw_string.split(" ")

        # Check to see if we got a full (verb included) or partial string
        if tokenized_verb_string[0].isupper():
            return tokenized_verb_string[0]

        return ''

    def rest(self):
        tokenized_verb_string = self.raw_string.split(" ")

        if len(tokenized_verb_string) > 1:
            return " ".join(tokenized_verb_string[1:])

        return ''

    def append(self, raw_string):
        tokenized_string = raw_string.split(" ")

        if len(tokenized_string) > 1:
            self.raw_string += " "
            self.raw_string += " ".join(tokenized_string[1:])
