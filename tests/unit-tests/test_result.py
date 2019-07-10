#!/usr/bin/env python
import re
from ldap_access_log_humanizer.result import Result


class TestResult():
    def test_creation(self):
        result = Result('RESULT tag=97 err=49 text=')
        assert isinstance(result, Result)
        assert result.tag() == 97
        assert result.err() == 49
        assert result.text() == ''
        assert result.verb() == 'RESULT'
        assert result.rest() == 'tag=97 err=49 text='
