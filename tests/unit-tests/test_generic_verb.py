#!/usr/bin/env python
import re
from ldap_access_log_humanizer.generic_verb import GenericVerb


class TestGenericVerb():
    def test_creation(self):
        generic_verb = GenericVerb('FOO bar')
        assert isinstance(generic_verb, GenericVerb)
        assert generic_verb.verb() == 'FOO'
        assert generic_verb.rest() == 'bar'
