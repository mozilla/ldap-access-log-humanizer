import re

# A class to parse and better understand RESULT and SEARCH RESULT strings


class Result:
    def __init__(self, raw_string):
        self.raw_string = raw_string

    def dict(self):
        return {
            "verb": self.verb(),
            "rest": self.rest(),
            "tag": self.tag(),
            "err": self.err(),
            "text": self.text()
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

    # Example: RESULT tag=97 err=49 text=
    # Output Expectation: 97
    def tag(self):
        pattern = r'tag=([0-9]+)'
        match = re.search(pattern, self.raw_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''

    def err(self):
        pattern = r'err=([0-9]+)'
        match = re.search(pattern, self.raw_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''

    def text(self):
        pattern = r'text="(.*)"'
        match = re.search(pattern, self.raw_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''
