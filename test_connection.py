#!/usr/bin/env python
from connection import Connection
import re


class TestConnection():
    def test_creation(self):
        connection = Connection(1245)
        assert isinstance(connection, Connection)
        assert connection.conn_id == 1245

    def test_parse_rest(self):
        rest = 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'

        connection = Connection(1245)
        connection.add_rest(rest)

        assert connection.conn_id == 1245
        assert connection.fd == 34
        assert connection.op == ""
        assert connection.verb == "ACCEPT"
        assert connection.verb_details == "from IP=192.168.1.1:56822 (IP=0.0.0.0:389)"
        assert connection.client == "192.168.1.1"

    def test_add_event(self):
        event = {'time': 'Oct 26 12:46:58',
                 'server': 'ldap.example.com',
                 'process': 'slapd[11086]',
                 'conn': '6862452',
                 'rest': 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'}

        connection = Connection(1245)
        connection.add_event(event)
        assert connection.time == event["time"]
        assert connection.server == event["server"]
        assert connection.process == event["process"]
        assert connection.conn_id == 1245
        assert connection.fd == 34
        assert connection.op == ""
        assert connection.verb == "ACCEPT"
        assert connection.verb_details == "from IP=192.168.1.1:56822 (IP=0.0.0.0:389)"
        assert connection.client == "192.168.1.1"
