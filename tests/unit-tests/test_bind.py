#!/usr/bin/env python
import re
from ldap_access_log_humanizer.bind import Bind


class TestBind():
    def test_creation(self):
        bind = Bind('dn="mail=user@example.com,o=com,dc=example" method=128 version=3')
        assert isinstance(bind, Bind)
<<<<<<< HEAD
        # TODO
        # assert operation.dn == 'mail=user@example.com,o=com,dc=example'
        # assert operation.o == 'com'
        # assert operation.dc == "example"
=======
        assert bind.dn() == 'mail=user@example.com,o=com,dc=example'
        assert bind.o() == 'com'
        assert bind.dc() == "example"
>>>>>>> fix_index_error_in_operation
        assert bind.mail() == "user@example.com"
        assert bind.version() == 3
        assert bind.method() == 128
