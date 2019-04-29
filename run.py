import argparse
import daemon
from daemon import pidfile
import os
import sys
import SocketServer
from humanizer import RawLogParser
from humanizer import Connection

LOG_FILE = 'humanizer.log'
HOST, PORT = "0.0.0.0", 1514
CONNECTIONS = {}

def parse(fp):

    for line in fp:
        parse_line(line)

def parse_line(line):
    # print(line.rstrip())
    # print("Active Connections: {}".format(len(connections)))

    event = RawLogParser().parse(line.rstrip())

    if event != None:

        # Look to see if we have an existing connection
        connection = CONNECTIONS.get(event['conn'])

        # If we have a pre-existing connection, just add context
        if connection:
            # print("Pre-existing connection: {}".format(str(event['conn'])))
            connection.add_event(event)

            # If the connection is closed, remove from active connections
            if connection.closed():
                CONNECTIONS.pop(event['conn'])

        # If it's a new connection, just create one and start tracking
        else:
            # print("New connection: {}".format(str(event['conn'])))
            connection = Connection(event['conn'])
            connection.add_event(event)
            CONNECTIONS[event['conn']] = connection

def syslog_server():
    server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
    server.serve_forever(poll_interval=0.5)

def start_daemon():
    pidf='/tmp/humanizer.pid'
    wdir = os.path.dirname(os.path.abspath(__file__))
    out = open(LOG_FILE, 'w+')
    with daemon.DaemonContext(
            working_directory=wdir,
            stdout=out,
            stderr=out,
            umask=0o002,
            pidfile=pidfile.TimeoutPIDLockFile(pidf),
            ) as context:
        syslog_server()

class SyslogUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        parse_line(str(data))

def main(prog_args = None):

    parser = argparse.ArgumentParser(
        description='Humanize (or flatten) an open-ldap log.')
    parser.add_argument('--file', help='path to open-ldap log file')
    parser.add_argument('--server', action='store_true',  help='run as syslog server')
    parser.add_argument('--daemonize', action='store_true',  help='run as daemon')
    args = parser.parse_args()

    if args.file:
        fp = open(args.file)
    elif args.server:
        if args.daemonize:
            start_daemon()
        else:
            syslog_server()
    else:
        fp = sys.stdin

    parse(fp)

if __name__ == "__main__":
    main()
