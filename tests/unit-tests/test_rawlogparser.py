#!/usr/bin/env python
from humanizer.raw_log_parser import RawLogParser


class TestRawLogParser():
    def test_line(self):
        log_line = "Oct 26 12:46:58 ldap.example.com slapd[11086]: conn=6862452 fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)"
        raw_log_parser = RawLogParser()
        expectation = {'time': 'Oct 26 12:46:58',
                       'server': 'ldap.example.com',
                       'process': 'slapd[11086]',
                       'conn': '6862452',
                       'rest': 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'}

        assert raw_log_parser.parse(log_line) == expectation

    def test_bad_line(self):
        log_line = "Oct 26 03:25:02 ldap.example.com slapd[11086]: connection_read(26): no connection!"
        raw_log_parser = RawLogParser()

        assert raw_log_parser.parse(log_line) == None
