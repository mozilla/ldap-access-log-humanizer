import re

# A class to parse and better understand RESULT strings


class Result:
    def __init__(self, raw_result_string):
        self.raw_result_string = raw_result_string

    # Example: RESULT tag=97 err=49 text=
    # Output Expectation: 97
    def tag(self):
        pattern = r'tag=([0-9]+)'
        match = re.search(pattern, self.raw_result_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''

    def err(self):
        pattern = r'err=([0-9]+)'
        match = re.search(pattern, self.raw_result_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''

    def text(self):
        pattern = r'text="(.*)"'
        match = re.search(pattern, self.raw_result_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''
