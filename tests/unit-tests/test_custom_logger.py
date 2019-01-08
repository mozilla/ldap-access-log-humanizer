#!/usr/bin/env python
import re
import pytest
import os
from humanizer.custom_logger import CustomLogger
import os


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

    def test_file_with_nonexistant_file(self):
        filename = "test_file_with_nonexistant_file.txt"

        # Clean up to make sure we don't have an existing file
        try:
            os.remove(filename)
        except Exception as e:
            pass

        # Try to log to a file that doesn't yet exist and make sure it creates it
        logger = CustomLogger("file", filename)
        assert os.path.isfile(filename) == False
        logger.log("hello world")
        assert os.path.isfile(filename) == True

        # Check to see if the content of the file is what we are expecting
        with open(filename) as f:
            s = f.read()
            assert s == "hello world" + "\n"

        # Clean up
        try:
            os.remove(filename)
        except Exception as e:
            pass

    def test_file_with_existant_file(self):
        filename = "test_file_with_existant_file.txt"

        # Clean up to make sure we don't have an existing file
        try:
            os.remove(filename)
        except Exception as e:
            pass

        with open(filename, "w") as f:
            f.write("hello world" + "\n")

        # Check to see if the content of the file is what we are expecting
        with open(filename) as f:
            s = f.read()
            assert s == "hello world" + "\n"

        # Try to log to a file that does exist and make sure it creates it
        logger = CustomLogger("file", filename)
        assert os.path.isfile(filename) == True
        logger.log("hello world")
        assert os.path.isfile(filename) == True

        # Check to see if the content of the file is what we are expecting
        with open(filename) as f:
            s = f.read()
            assert s == "hello world" + "\n" + "hello world" + "\n"

        # Clean up
        try:
            os.remove(filename)
        except Exception as e:
            pass
