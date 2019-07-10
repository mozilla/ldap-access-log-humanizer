import re

# A class to parse and better understand BIND strings


class Bind:
    def __init__(self, raw_bind_string):
        self.raw_bind_string = raw_bind_string

    # Example: BIND dn="mail=user@example.com,o=com,dc=example"
    # Output Expectation: user@example.com
    def mail(self):
        # Regex stolen from: https://stackoverflow.com/questions/42407785/regex-extract-email-from-strings
        pattern = r'mail=([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
        match = re.search(pattern, self.raw_bind_string)
        if match:
            return match.group(1)

        # If we don't exact match, default to unknown
        return ''

    def version(self):
        pattern = r'version=([0-3]+)'
        match = re.search(pattern, self.raw_bind_string)
        if match:
            return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''

    def method(self):
        pattern = r'method=(0|128|sasl)'
        match = re.search(pattern, self.raw_bind_string)
        if match:
            if match.group(1) == "sasl":
                return match.group(1)
            else:
                return int(match.group(1))

        # If we don't exact match, default to unknown
        return ''
<<<<<<< HEAD
=======

    def dn(self):
        pattern = r'dn="(.*)"'
        match = re.search(pattern, self.raw_bind_string)
        if match:
            if match.group(1):
                return match.group(1)

        # If we don't exact match, default to unknown
        return ''

    def o(self):
        pattern = r'o=([a-zA-Z0-9]+)'
        match = re.search(pattern, self.raw_bind_string)
        if match:
            if match.group(1):
                return match.group(1)

        # If we don't exact match, default to unknown
        return ''

    def dc(self):
        pattern = r'dc=([a-zA-Z0-9]+)'
        match = re.search(pattern, self.raw_bind_string)
        if match:
            if match.group(1):
                return match.group(1)

        # If we don't exact match, default to unknown
        return ''
>>>>>>> fix_index_error_in_operation
