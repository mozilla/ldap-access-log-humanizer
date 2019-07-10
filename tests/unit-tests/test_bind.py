#!/usr/bin/env python
import re
from ldap_access_log_humanizer.bind import Bind


class TestBind():
    def test_creation(self):
        bind = Bind('BIND dn="mail=user@example.com,o=com,dc=example" method=128 version=3')
        assert isinstance(bind, Bind)
        assert bind.dn() == 'mail=user@example.com,o=com,dc=example'
        assert bind.o() == 'com'
        assert bind.dc() == "example"
        assert bind.mail() == "user@example.com"
        assert bind.version() == 3
        assert bind.method() == 128
        assert bind.verb() == 'BIND'
        assert bind.rest() == 'dn="mail=user@example.com,o=com,dc=example" method=128 version=3'
        assert bind.raw_string == 'BIND dn="mail=user@example.com,o=com,dc=example" method=128 version=3'

    def test_append(self):
        bind = Bind('BIND dn="mail=user@example.com,o=com,dc=example" method=128 version=3')
        assert isinstance(bind, Bind)
        assert bind.raw_string == 'BIND dn="mail=user@example.com,o=com,dc=example" method=128 version=3'

        # Add a new item to the list
        bind_cont = 'BIND foo=1'
        bind.append(bind_cont)
        assert bind.raw_string == 'BIND dn="mail=user@example.com,o=com,dc=example" method=128 version=3 foo=1'
