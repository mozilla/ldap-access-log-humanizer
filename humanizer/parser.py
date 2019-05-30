from humanizer.raw_log_parser import RawLogParser
from humanizer.connection import Connection


class Parser:
    def __init__(self, fp, args_dict):
        self.fp = fp
        self.args_dict = args_dict
        self.connections = {}

    def parse(self):
        for line in self.fp:
            self.parse_line(line)

    def parse_line(self, line):
        event = RawLogParser(self.args_dict).parse(line.rstrip())

        if event is not None:

            # Look to see if we have an existing connection
            connection = self.connections.get(event["conn"])

            # If we have a pre-existing connection, just add context
            if connection:
                connection.add_event(event)

                # If the connection is closed, remove from active connections
                if connection.closed():
                    self.connections.pop(event["conn"])

            # If it's a new connection, just create one and start tracking
            else:
                connection = Connection(event["conn"], self.args_dict)
                connection.add_event(event)
                self.connections[event["conn"]] = connection
