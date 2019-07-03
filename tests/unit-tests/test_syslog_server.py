#!/usr/bin/env python
from ldap_access_log_humanizer.syslog_server import CustomSyslogUDPHandler
from ldap_access_log_humanizer.syslog_server import UDPServer
from ldap_access_log_humanizer.syslog_server import SyslogServer
from ldap_access_log_humanizer.parser import Parser


class TestSyslogServer():
    # Note: this doesn't actually test the class directly, it just tests the logic within the class to verify functionality is as expected
    def test_handle(self):
        args_dict = {'output_mozdef': False, 'output_stdout': True, 'input_type': 'file', 'output_file': False, 'output_syslog': False,
                     'host': '0.0.0.0', 'daemonize': False, 'input_file_name': None, 'mozdef_url': 'https://127.0.0.1:8443/events',
                     'noconfig': False, 'output_file_name': 'humanizer.log', 'output_stderr': False, 'config': 'humanizer_settings.json',
                     'port': '1514', 'syslog_facility': 'LOG_LOCAL5', 'verbose': True}

        log_lines = [
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 fd=28 ACCEPT from IP=127.0.0.1:44182 (IP=0.0.0.0:389)',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=0 EXT oid=1.3.6.1.4.1.1466.20037',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=0 STARTTLS',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=0 RESULT oid= err=0 text=',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 fd=28 TLS established tls_ssf=256 ssf=256',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=1 BIND dn="uid=nagioscheck,ou=logins,dc=mozilla" method=128',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=1 BIND dn="uid=nagioscheck,ou=logins,dc=mozilla" mech=SIMPLE ssf=0',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=1 RESULT tag=97 err=0 text=',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=2 SRCH base="dc=mozilla" scope=0 deref=0 filter="(objectClass=*)"',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=2 SEARCH RESULT tag=101 err=0 nentries=1 text=',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 op=3 UNBIND',
            '<167>Jul  2 19:40:26 slave1.ldap.mdc1.mozilla.com slapd[5436]: conn=1150013 fd=28 closed'
        ]

        parser = Parser(None, args_dict)
        assert len(parser.connections) == 0

        for log in log_lines:
            new_log = log.lstrip('<167>')
            assert new_log.startswith('<167>') == False
            parser.parse_line(new_log)
            assert isinstance(parser.connections, dict)
            # All of our test data is from a single connection (so it will only ever be 1, until the close)
            if new_log.endswith('closed'):
                assert len(parser.connections) == 0
            else:
                assert len(parser.connections) == 1

        # This is zeroed out after because the connection is gone at this point
        assert len(parser.connections) == 0
