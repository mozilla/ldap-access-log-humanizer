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
        assert connection.error == ""

    def test_add_event_accept(self):
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
        assert connection.error == ""

    def test_add_event_ext(self):
        event = {'time': 'Oct 26 12:46:58',
                 'server': 'ldap.example.com',
                 'process': 'slapd[11086]',
                 'conn': '6862452',
                 'rest': 'op=0 EXT oid=1.3.6.1.4.1.1466.20037'}

        connection = Connection(1245)
        connection.add_event(event)
        assert connection.time == event["time"]
        assert connection.server == event["server"]
        assert connection.process == event["process"]
        assert connection.conn_id == 1245
        assert connection.fd == ""
        assert connection.op == 0
        assert connection.verb == "EXT"
        assert connection.verb_details == "oid=1.3.6.1.4.1.1466.20037"
        assert connection.error == ""

    def test_add_event_starttls(self):
        event = {'time': 'Oct 26 12:46:58',
                 'server': 'ldap.example.com',
                 'process': 'slapd[11086]',
                 'conn': '6862452',
                 'rest': 'op=0 STARTTLS'}

        connection = Connection(1245)
        connection.add_event(event)
        assert connection.time == event["time"]
        assert connection.server == event["server"]
        assert connection.process == event["process"]
        assert connection.conn_id == 1245
        assert connection.fd == ""
        assert connection.op == 0
        assert connection.verb == "STARTTLS"
        assert connection.verb_details == ""
        assert connection.error == ""

    def test_add_event_result(self):
        event = {'time': 'Oct 26 12:46:58',
                 'server': 'ldap.example.com',
                 'process': 'slapd[11086]',
                 'conn': '6862452',
                 'rest': 'op=0 RESULT oid= err=0 text='}

        connection = Connection(1245)
        connection.add_event(event)
        assert connection.time == event["time"]
        assert connection.server == event["server"]
        assert connection.process == event["process"]
        assert connection.conn_id == 1245
        assert connection.fd == ""
        assert connection.op == 0
        assert connection.verb == "RESULT"
        assert connection.verb_details == "oid= err=0 text="
        assert connection.error == ""

    def test_add_event_result(self):
        event = {'time': 'Oct 26 12:46:58',
                 'server': 'ldap.example.com',
                 'process': 'slapd[11086]',
                 'conn': '6862452',
                 'rest': 'fd=34 TLS established tls_ssf=256 ssf=256'}

        connection = Connection(1245)
        connection.add_event(event)
        assert connection.time == event["time"]
        assert connection.server == event["server"]
        assert connection.process == event["process"]
        assert connection.conn_id == 1245
        assert connection.fd == 34
        assert connection.op == ""
        assert connection.verb == "TLS"
        assert connection.verb_details == "established tls_ssf=256 ssf=256"
        assert connection.error == ""

    def test_add_event_bind(self):
        event = {'time': 'Oct 26 12:46:58',
                 'server': 'ldap.example.com',
                 'process': 'slapd[11086]',
                 'conn': '6862452',
                 'rest': 'op=1 BIND dn="mail=user@example.com,o=com,dc=example" method=128'}

        connection = Connection(1245)
        connection.add_event(event)
        assert connection.time == event["time"]
        assert connection.server == event["server"]
        assert connection.process == event["process"]
        assert connection.conn_id == 1245
        assert connection.fd == ""
        assert connection.op == 1
        assert connection.verb == "BIND"
        assert connection.verb_details == 'dn="mail=user@example.com,o=com,dc=example" method=128'
        assert connection.error == ""

    def test_add_event_result(self):
        event = {'time': 'Oct 26 12:46:58',
                 'server': 'ldap.example.com',
                 'process': 'slapd[11086]',
                 'conn': '6862452',
                 'rest': 'op=1 RESULT tag=97 err=49 text='}

        connection = Connection(1245)
        connection.add_event(event)
        assert connection.time == event["time"]
        assert connection.server == event["server"]
        assert connection.process == event["process"]
        assert connection.conn_id == 1245
        assert connection.fd == ""
        assert connection.op == 1
        assert connection.verb == "RESULT"
        assert connection.verb_details == 'tag=97 err=49 text='
        assert connection.error == "LDAP_INVALID_CREDENTIALS"

    def test_add_event_log(self):
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
        assert connection.error == ""
        assert connection.log() == {'client': '192.168.1.1',
                                    'conn_id': 1245,
                                    'fd': 34,
                                    'op': '',
                                    'time': 'Oct 26 12:46:58',
                                    'tls': False,
                                    'verb': 'ACCEPT',
                                    'error': '',
                                    'verb_details': 'from IP=192.168.1.1:56822 (IP=0.0.0.0:389)',
                                    'process': 'slapd[11086]',
                                    'server': 'ldap.example.com'}
