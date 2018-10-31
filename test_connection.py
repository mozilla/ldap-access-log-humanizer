#!/usr/bin/env python
from connection import Connection
import re


class TestConnection():
    def test_creation(self):
        connection = Connection(1245)
        assert isinstance(connection, Connection)
        assert connection.conn_id == 1245

    def test_parse_generic_file_descriptor(self):
        rest = 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'

        connection = Connection(1245)
        connection.add_rest(rest)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0

    def test_parse_generic_operation(self):
        rest = 'op=1 BIND dn="mail=user@example.com,o=com,dc=example" method=128'

        connection = Connection(1245)
        connection.add_rest(rest)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 1

    def test_tls_established(self):
        rest = 'fd=34 TLS established tls_ssf = 256 ssf = 256'

        connection = Connection(1245)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.tls() == False

        connection.add_rest(rest)
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0
        assert connection.tls() == True

    def test_accept(self):
        rest = 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'

        connection = Connection(1245)

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

        connection = Connection(1245)

        assert connection.conn_id == 1245
        assert len(connection.file_descriptors) == 0
        assert len(connection.operations) == 0
        assert connection.closed() == False

        connection.add_rest(rest)
        assert len(connection.file_descriptors) == 1
        assert len(connection.operations) == 0
        assert connection.closed() == True
