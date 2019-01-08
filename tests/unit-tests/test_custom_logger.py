#!/usr/bin/env python
import re
import pytest
import os
from humanizer.custom_logger import CustomLogger


class TestCustomLogger():
    def test_creation(self):
        logger = CustomLogger("stdout")
        assert isinstance(logger, CustomLogger)

    def test_stdout(self, capsys):
        logger = CustomLogger("stdout")
        logger.log("hello world")
        out, err = capsys.readouterr()
        assert out == "hello world\n"
        assert err == ""

    def test_stderr(self, capsys):
        logger = CustomLogger("stderr")
        logger.log("hello world")
        out, err = capsys.readouterr()
        assert out == ""
        assert err == "hello world\n"

    def test_file_with_no_file(self):
        logger = CustomLogger("file")
        with pytest.raises(Exception) as excinfo:
            logger.log("hello world")
        assert str(excinfo.value) == 'log_type of "file" was chosen, but no log file specified'
