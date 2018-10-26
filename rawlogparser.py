import re


class RawLogParser:
    def parse(self, line):
        # This regex takes a raw log and parses it into a few elements
        # time, server, process, and arbitrary remainder
        pattern = r'^(\w+ \d+ \d+:\d+:\d+) ([a-zA-Z0-9\.]+) (\w+\[\d+\]): conn=(\d+) (.*)$'
        match = re.search(pattern, line)

        if match:
            return {'time': match[1],
                    'server': match[2],
                    'process': match[3],
                    'conn': match[4],
                    'rest': match[5]}
        else:
            raise Exception('Failed to parse raw line: {}'.format(line))
