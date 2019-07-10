import re

# A class to parse and better understand BIND strings


class GenericVerb:
    def __init__(self, raw_generic_verb_string):
        self.raw_generic_verb_string = raw_generic_verb_string

    def verb(self):
        tokenized_verb_string = self.raw_generic_verb_string.split(" ")

        # Check to see if we got a full (verb included) or partial string
        if tokenized_verb_string[0].isupper():
            return tokenized_verb_string[0]

        return ''

    def rest(self):
        tokenized_verb_string = self.raw_generic_verb_string.split(" ")

        if len(tokenized_verb_string) > 1:
            return " ".join(tokenized_verb_string[1:])

        return ''
