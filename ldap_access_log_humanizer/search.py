import re

# A class to parse and better understand SRCH strings


class Search:
    def __init__(self, raw_string):
        self.raw_string = raw_string

    def dict(self):
        return {
            "verb": self.verb(),
            "rest": self.rest(),
            "base": self.base(),
            "scope": self.scope(),
            "deref": self.deref(),
            "filter": self.filter()

        }

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

    def base(self):
        pattern = r'base="([a-zA-Z0-9=,]+)"'
        match = re.search(pattern, self.raw_string)
        if match:
            return match.group(1)

        # If we don't exact match, default to unknown
        return ''

    def scope(self):
        pattern = r'scope=([0-9]+)'
        match = re.search(pattern, self.raw_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''

    def deref(self):
        pattern = r'deref=([0-9]+)'
        match = re.search(pattern, self.raw_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''

    def filter(self):
        pattern = r'filter="([a-zA-Z0-9=_\(\)]+)"'
        match = re.search(pattern, self.raw_string)
        if match:
            return match.group(1)

        # If we don't exact match, default to unknown
        return ''
