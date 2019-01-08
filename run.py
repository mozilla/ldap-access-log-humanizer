import argparse
import sys
from humanizer import RawLogParser
from humanizer import Connection

parser = argparse.ArgumentParser(
    description='Humanize (or flatten) an open-ldap log.')
parser.add_argument('--file', help='path to open-ldap log file')
args = parser.parse_args()

# Used for connection tracking
connections = {}

if args.file:
    fp = open(args.file)
else:
    fp = sys.stdin

for line in fp:
    # print(line.rstrip())
    # print("Active Connections: {}".format(len(connections)))

    event = RawLogParser().parse(line.rstrip())

    if event == None:
        continue

    # Look to see if we have an existing connection
    connection = connections.get(event['conn'])

    # If we have a pre-existing connection, just add context
    if connection:
        # print("Pre-existing connection: {}".format(str(event['conn'])))
        connection.add_event(event)

        # If the connection is closed, remove from active connections
        if connection.closed():
            connections.pop(event['conn'])

    # If it's a new connection, just create one and start tracking
    else:
        # print("New connection: {}".format(str(event['conn'])))
        connection = Connection(event['conn'])
        connection.add_event(event)
        connections[event['conn']] = connection
