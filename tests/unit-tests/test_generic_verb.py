#!/usr/bin/env python
import re
from ldap_access_log_humanizer.generic_verb import GenericVerb


class TestGenericVerb():
    def test_creation(self):
        generic_verb = GenericVerb('FOO bar')
        assert isinstance(generic_verb, GenericVerb)
        assert generic_verb.verb() == 'FOO'
        assert generic_verb.rest() == 'bar'

    def test_append(self):
        generic_verb = GenericVerb('FOO bar')
        assert isinstance(generic_verb, GenericVerb)
        assert generic_verb.raw_string == 'FOO bar'

        # Add a new item to the list
        generic_cont = 'FOO baz'
        generic_verb.append(generic_cont)
        assert generic_verb.raw_string == 'FOO bar baz'
