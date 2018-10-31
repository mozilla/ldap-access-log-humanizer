#!/usr/bin/env python
from file_descriptor import FileDescriptor
import re


class TestFileDescriptor():
    def test_creation(self):
        file_descriptor = FileDescriptor(0)
        assert isinstance(file_descriptor, FileDescriptor)
        assert file_descriptor.fd_id == 0
        assert file_descriptor.verb == ""
        assert file_descriptor.details == ""

    def test_add_accept(self):
        rest = 'ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)'

        file_descriptor = FileDescriptor(0)
        file_descriptor.add_event(rest)

        assert isinstance(file_descriptor, FileDescriptor)
        assert file_descriptor.fd_id == 0
        assert file_descriptor.verb == "ACCEPT"
        assert file_descriptor.details == "from IP=192.168.1.1:56822 (IP=0.0.0.0:389)"

    def test_add_tls(self):
        rest = 'TLS established tls_ssf=256 ssf=256'

        file_descriptor = FileDescriptor(0)
        file_descriptor.add_event(rest)

        assert isinstance(file_descriptor, FileDescriptor)
        assert file_descriptor.fd_id == 0
        assert file_descriptor.verb == "TLS"
        assert file_descriptor.details == "established tls_ssf=256 ssf=256"

    def test_add_closed(self):
        rest = 'closed'

        file_descriptor = FileDescriptor(0)
        file_descriptor.add_event(rest)

        assert isinstance(file_descriptor, FileDescriptor)
        assert file_descriptor.fd_id == 0
        assert file_descriptor.verb == "closed"
        assert file_descriptor.details == ""
