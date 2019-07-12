#!/usr/bin/env python
import re
from ldap_access_log_humanizer.search import Search


class TestSearch():
    def test_creation(self):
        search = Search('SRCH base="ou=groups,dc=example" scope=2 deref=0 filter="(cn=group_name)"')
        assert isinstance(search, Search)
        assert search.verb() == 'SRCH'
        assert search.rest() == 'base="ou=groups,dc=example" scope=2 deref=0 filter="(cn=group_name)"'
        assert search.base() == 'ou=groups,dc=example'
        assert search.scope() == 2
        assert search.deref() == 0
        assert search.filter() == '(cn=group_name)'

    def test_append(self):
        search = Search('SRCH base="ou=groups,dc=example" scope=2 deref=0 filter="(cn=group_name)"')
        assert isinstance(search, Search)
        assert search.raw_string == 'SRCH base="ou=groups,dc=example" scope=2 deref=0 filter="(cn=group_name)"'

        # Add a new item to the list
        generic_cont = 'SRCH attr=memberUid'
        search.append(generic_cont)
        assert search.raw_string == 'SRCH base="ou=groups,dc=example" scope=2 deref=0 filter="(cn=group_name)" attr=memberUid'
