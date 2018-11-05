#!/usr/bin/env python
import re
from humanizer.operation import Operation


class TestOperation():
    def test_creation(self):
        operation = Operation(0)
        assert isinstance(operation, Operation)
        assert operation.op_id == 0
        assert operation.requests == []
        assert operation.response_verb == ""
        assert operation.response_verb_details == set()

    def test_add_bind(self):
        rest = 'BIND dn="uid=bind-generateusers,ou=logins,dc=example" method=128'

        operation = Operation(0)
        operation.add_event(rest)

        assert isinstance(operation, Operation)
        assert operation.op_id == 0
        assert operation.requests == [{"verb": "BIND", "details": [
            'dn="uid=bind-generateusers,ou=logins,dc=example"', 'method=128']}]
        assert operation.response_verb == ""
        assert operation.response_verb_details == set()

    def test_add_bind_multiple(self):
        rest = 'BIND dn="uid=bind-generateusers,ou=logins,dc=example" method=128'
        rest2 = 'BIND dn="uid=bind-generateusers,ou=logins,dc=example" mech=SIMPLE ssf=0'

        operation = Operation(0)
        operation.add_event(rest)
        operation.add_event(rest2)

        assert isinstance(operation, Operation)
        assert operation.op_id == 0
        assert operation.requests == [{"verb": "BIND", "details": ['dn="uid=bind-generateusers,ou=logins,dc=example"', 'method=128', 'mech=SIMPLE', 'ssf=0']}]
        assert operation.response_verb == ""
        assert operation.response_verb_details == set()

    def test_add_bind_multiple_with_result(self):
        rest = 'BIND dn="uid=bind-generateusers,ou=logins,dc=example" method=128'
        rest2 = 'BIND dn="uid=bind-generateusers,ou=logins,dc=example" mech=SIMPLE ssf=0'
        rest3 = 'RESULT tag=97 err=0 text='

        operation = Operation(0)
        operation.add_event(rest)
        operation.add_event(rest2)
        operation.add_event(rest3)

        assert isinstance(operation, Operation)
        assert operation.op_id == 0
        assert operation.requests == [
            {'details': [
                'dn="uid=bind-generateusers,ou=logins,dc=example"',
                'method=128',
                'mech=SIMPLE',
                'ssf=0'
            ],
                'verb': 'BIND'
            }]
        assert operation.response_verb == "RESULT"
        assert operation.response_verb_details == set(
            ['tag=97', 'err=0', 'text='])
        assert operation.loggable() == True
        assert operation.dict() == {'op_id': 0,
                                    'requests': [
                                        {'details': [
                                            'dn="uid=bind-generateusers,ou=logins,dc=example"',
                                            'method=128'
                                            'mech=SIMPLE',
                                            'ssf=0'
                                        ],
                                            'verb': 'BIND'
                                        }],
                                    'response': {
                                        'verb': 'RESULT',
                                        'details': [
                                            'err=0',
                                            'tag=97',
                                            'text='
                                        ],
                                        'error': 'LDAP_SUCCESS'
                                    }}

    def test_add_search_multiple_with_result(self):
        rest = 'SRCH base="ou=groups,dc=example" scope=2 deref=0 filter="(cn=group_name)"'
        rest2 = 'SRCH attr=memberUid'
        rest3 = 'SEARCH RESULT tag=101 err=0 nentries=1 text='

        operation = Operation(0)
        operation.add_event(rest)
        operation.add_event(rest2)
        operation.add_event(rest3)

        assert isinstance(operation, Operation)
        assert operation.op_id == 0
        assert operation.requests == [
            {
                'details': [
                    'base="ou=groups,dc=example"',
                    'scope=2',
                    'deref=0',
                    'filter="(cn=group_name)"',
                    'attr=memberUid'
                ],
                'verb': 'SRCH'
            }
        ]
        assert operation.response_verb == "SEARCH RESULT"
        assert operation.response_verb_details == set(
            ['tag=101', 'err=0', 'nentries=1', 'text='])
        assert operation.loggable() == True
        assert operation.dict() == {'op_id': 0,
                                    'requests': [
                                        {
                                            'details': [
                                                'base="ou=groups,dc=example"',
                                                'scope=2',
                                                'deref=0',
                                                'filter="(cn=group_name)"'
                                            ],
                                            'verb': 'SRCH'
                                        },
                                        {
                                            'details': [
                                                'attr=memberUid'
                                            ],
                                            'verb': 'SRCH'
                                        }
                                    ],
                                    'response': {
                                        'details': [
                                            'err=0',
                                            'nentries=1',
                                            'tag=101',
                                            'text='
                                        ],
                                        'verb': 'SEARCH RESULT',
                                        'error': 'LDAP_SUCCESS'
                                    }}
