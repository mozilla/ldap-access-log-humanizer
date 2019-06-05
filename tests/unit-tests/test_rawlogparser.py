#!/usr/bin/env python
from ldap_access_log_humanizer.raw_log_parser import RawLogParser


TEST_RAW_LOG_PARSER_ARGS_DICT = {'output_mozdef': False, 'output_stdout': True, 'input_type': 'file', 'output_file': False, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False,
                                 'input_file_name': None, 'mozdef_url': 'https://127.0.0.1:8443/events', 'noconfig': False, 'output_file_name': 'humanizer.log', 'output_stderr': False, 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5'}


class TestRawLogParser():
    def test_line(self):
        log_line = "Oct 26 12:46:58 ldap.example.com slapd[11086]: conn=6862452 fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)"
        raw_log_parser = RawLogParser(args_dict)
        expectation = {'time': 'Oct 26 12:46:58',
                       'server': 'ldap.example.com',
                       'process': 'slapd[11086]',
                       'conn': '6862452',
                       'rest': 'fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'}

        assert raw_log_parser.parse(log_line) == expectation

    def test_bad_line(self):
        log_line = "Oct 26 03:25:02 ldap.example.com slapd[11086]: connection_read(26): no connection!"
        raw_log_parser = RawLogParser(TEST_RAW_LOG_PARSER_ARGS_DICT)

        assert raw_log_parser.parse(log_line) == None
