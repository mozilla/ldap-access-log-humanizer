import argparse
import json
import os
import sys
from ldap_access_log_humanizer import Parser
from ldap_access_log_humanizer import SyslogServer


def main(prog_args=None):

    # In the interest of being flexible until we finalize on the use case, this
    # script takes a myriad of command line options optionally, or can read
    # the entire config from a config file. Currently config file overrides all
    # config options, unless you specify --noconfig, in which case config file
    # is ignored and you must supply all command line options or rely on
    # defaults.

    parser = argparse.ArgumentParser(description="Humanize (or flatten) an open-ldap log.")
    parser.add_argument("--daemonize", action="store_true", help="run as daemon")
    parser.add_argument("--input_type", default="stdin", help="input type")
    parser.add_argument("--input_file_name", help="path to open-ldap log file")
    parser.add_argument("--host", default="0.0.0.0", help="IP to listen on")
    parser.add_argument("--port", default="1514", help="port to listen on")
    parser.add_argument("--output_syslog", action="store_true", help="output to syslog")
    parser.add_argument("--output_mozdef", action="store_true", help="output to mozdef")
    parser.add_argument("--output_stdout", action="store_true", help="output to stdout")
    parser.add_argument("--output_stderr", action="store_true", help="output to stderr")
    parser.add_argument("--output_file", action="store_true", help="output to file")
    parser.add_argument("--output_file_name", default="humanizer.log", help="output file path")
    parser.add_argument("--mozdef_url", default="https://127.0.0.1:8443/events", help="mozdef url")
    parser.add_argument("--config", default="humanizer_settings.json", help="config file path")
    parser.add_argument("--noconfig", action="store_true", help="use cli options instead of config")
    args = parser.parse_args()
    args_dict = vars(args)

    if not args.noconfig:
        if args.config:
            with open(args.config) as fd:
                args_dict = json.load(fd)
        else:
            __location__ = os.path.dirname(__file__)
            with open(os.path.join(__location__, "humanizer_settings.json")) as fd:
                args_dict = json.load(fd)

    # Once we've figured out which configuration we are using, we set the fp var
    # to the input method of choice and go into the business of parsing the input
    if args_dict["input_type"] == "stdin":
        fp = sys.stdin
    elif args_dict["input_type"] == "file":
        fp = open(args_dict["input_file_name"])
    elif args_dict["input_type"] == "syslog":
        syslog_server = SyslogServer(fp, args_dict)
        syslog_server.start_syslog()

    # The syslog server handles the parsing directly, but if we've chosen
    # file or stdin, then we need to go ahead and get on to parsing directly
    if args_dict["input_type"] == "stdin" or args_dict["input_type"] == "file":
        log_parser = Parser(fp, args_dict)
        log_parser.parse()


if __name__ == "__main__":
    main()
