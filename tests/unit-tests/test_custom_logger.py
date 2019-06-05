#!/usr/bin/env python
import re
import pytest
import os
from ldap_access_log_humanizer.custom_logger import CustomLogger
import os

TEST_CUSTOM_LOGGER_ARGS_DICT = {'output_mozdef': False, 'output_stdout': True, 'input_type': 'file', 'output_file': False, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False,
                                'input_file_name': None, 'mozdef_url': 'https://127.0.0.1:8443/events', 'noconfig': False, 'output_file_name': 'humanizer.log', 'output_stderr': False, 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5'}


class TestCustomLogger():
    def test_creation(self):
        logger = CustomLogger(TEST_CUSTOM_LOGGER_ARGS_DICT)
        assert isinstance(logger, CustomLogger)

    def test_default(self, capsys):
        logger = CustomLogger(TEST_CUSTOM_LOGGER_ARGS_DICT)
        logger.log("hello world")
        out, err = capsys.readouterr()
        assert out == "hello world\n"
        assert err == ""

    def test_stdout(self, capsys):
        logger = CustomLogger(TEST_CUSTOM_LOGGER_ARGS_DICT)
        logger.log("hello world")
        out, err = capsys.readouterr()
        assert out == "hello world\n"
        assert err == ""

    def test_stderr(self, capsys):
        args_dict = {'output_mozdef': False, 'output_stdout': False, 'output_stderr': True, 'input_type': 'file', 'output_file': False, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False, 'input_file_name': None,
                     'mozdef_url': 'https://127.0.0.1:8443/events', 'noconfig': False, 'output_file_name': 'humanizer.log', 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5'}

        logger = CustomLogger(args_dict)
        logger.log("hello world")
        out, err = capsys.readouterr()
        assert out == ""
        assert err == "hello world\n"

    def test_file_with_blank_file(self):
        args_dict = {'output_mozdef': False, 'output_stdout': False, 'input_type': 'file', 'output_file': True, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False,
                     'input_file_name': None, 'mozdef_url': 'https://127.0.0.1:8443/events', 'noconfig': False, 'output_file_name': '', 'output_stderr': False, 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5', 'verbose': True}
        logger = CustomLogger(TEST_CUSTOM_LOGGER_ARGS_DICT)
        with pytest.raises(Exception) as excinfo:
            logger.log("hello world")
        assert str(excinfo.value) == 'log_type of "file" was chosen, but no log file specified'

    def test_file_with_no_file(self):
        args_dict = {'output_mozdef': False, 'output_stdout': False, 'input_type': 'file', 'output_file': True, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False,
                     'input_file_name': None, 'mozdef_url': 'https://127.0.0.1:8443/events', 'noconfig': False, 'output_stderr': False, 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5', 'verbose': True}
        logger = CustomLogger(TEST_CUSTOM_LOGGER_ARGS_DICT)
        with pytest.raises(Exception) as excinfo:
            logger.log("hello world")
        assert str(excinfo.value) == 'log_type of "file" was chosen, but no log file specified'

    def test_file_with_nonexistant_file(self):
        filename = "test_file_with_nonexistant_file.txt"
        args_dict = {'output_mozdef': False, 'output_stdout': False, 'input_type': 'file', 'output_file': True, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False, 'input_file_name': None,
                     'mozdef_url': 'https://127.0.0.1:8443/events', 'noconfig': False, 'output_file_name': filename, 'output_stderr': False, 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5', 'verbose': True}

        # Clean up to make sure we don't have an existing file
        try:
            os.remove(filename)
        except Exception as e:
            pass

        # Try to log to a file that doesn't yet exist and make sure it creates it
        logger = CustomLogger(args_dict)
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
        args_dict = {'output_mozdef': False, 'output_stdout': False, 'input_type': 'file', 'output_file': True, 'output_syslog': False, 'host': '0.0.0.0', 'daemonize': False, 'input_file_name': None,
                     'mozdef_url': 'https://127.0.0.1:8443/events', 'noconfig': False, 'output_file_name': filename, 'output_stderr': False, 'config': 'humanizer_settings.json', 'port': '1514', 'syslog_facility': 'LOG_LOCAL5', 'verbose': True}

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
        logger = CustomLogger(args_dict)
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
