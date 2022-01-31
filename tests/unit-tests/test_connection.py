#!/usr/bin/env python
import re
import pytest
import sys
import os
from ldap_access_log_humanizer.connection import Connection

TEST_CONNECTION_ARGS_DICT = {'output_stdout': True, 'input_type': 'file', 'output_file': False, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False, 'input_file_name': None,
                             'noconfig': False, 'output_file_name': 'humanizer.log', 'output_stderr': False, 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5'}


class TestConnection():

    def test_creation(self):
        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)
        assert isinstance(connection, Connection)
        assert connection.conn_id == 1245

    def test_parse_generic_file_descriptor(self):
        rest = 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)
        connection.add_rest(rest)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0

    def test_parse_generic_operation(self):
        rest = 'op=1 BIND dn="mail=user@example.com,o=com,dc=example" method=128'

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)
        connection.add_rest(rest)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 1

    def test_authenticated_mail(self):
        rest1 = 'op=1 BIND dn="mail=user@example.com,o=com,dc=example" method=128'
        rest2 = 'op=1 RESULT tag=97 err=0 text='

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.authenticated() == False
        assert connection.user == ""

        connection.add_rest(rest1)
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 1
        assert connection.authenticated() == False
        assert connection.user == "user@example.com"

        connection.add_rest(rest2)
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 1
        assert connection.authenticated() == True
        assert connection.user == "user@example.com"

    def test_authenticated_uid(self):
        rest1 = 'op=1 BIND dn="uid=foo-bar,ou=logins,dc=mozilla" method=128 mech=SIMPLE method=128 ssf=0'
        rest2 = 'op=1 RESULT tag=97 err=0 text='

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.authenticated() == False
        assert connection.user == ""

        connection.add_rest(rest1)
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 1
        assert connection.authenticated() == False
        assert connection.user == "foo-bar"

        connection.add_rest(rest2)
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 1
        assert connection.authenticated() == True
        assert connection.user == "foo-bar"

    def test_tls_established(self):
        rest = 'fd=34 TLS established tls_ssf = 256 ssf = 256'

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.tls() == False

        connection.add_rest(rest)
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0
        assert connection.tls() == True

    def test_persistent_tls_established(self):
        rest1 = 'fd=34 TLS established tls_ssf = 256 ssf = 256'
        rest2 = 'fd=34 FOO bar tls_ssf = 256 ssf = 256'

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.tls() == False

        connection.add_rest(rest1)
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0
        assert connection.tls() == True

        # Adding another rest, to ensure TLS is persistent through connection
        connection.add_rest(rest2)
        assert len(connection.file_descriptors) == 2
        assert len(connection.operations) == 0
        assert connection.tls() == True

    def test_accept(self):
        rest = 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.client() == ''

        connection.add_rest(rest)
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0
        assert connection.client() == '192.168.1.1'

    def test_closed(self):
        rest = 'fd=34 closed'

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.closed() == False

        connection.add_rest(rest)
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0
        assert connection.closed() == True

    def test_dict(self):
        event = {'time': "now",
                 'server': "foo.example.com",
                 'process': "slapd[1]",
                 'rest': 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'}

        connection = Connection(1245, TEST_CONNECTION_ARGS_DICT)
        connection.add_event(event)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0

        assert connection.dict() == {'authenticated': False,
                                     'client': '192.168.1.1',
                                     'conn_id': 1245,
                                     'server': 'foo.example.com',
                                     'time': 'now',
                                     'tls': False,
                                     'user': ''}
