import datetime
import os
import requests
import socket
import sys
import syslog
import requests


class CustomLogger:
    # Here we deal with specific output types. This class supports
    # many different output types and it can handle them simultaneously
    def __init__(self, args_dict):
        self.output_syslog = args_dict['output_syslog']
        self.output_mozdef = args_dict['output_mozdef']
        self.output_stdout = args_dict['output_stdout']
        self.output_stderr = args_dict['output_stderr']
        self.output_file = args_dict['output_file']
        self.output_file_name = args_dict['output_file_name']
        self.mozdef_url = args_dict['mozdef_url']

    def log(self, data):
        if self.output_stdout:
            print(str(data))
        if self.output_stderr:
            sys.stderr.write(str(data) + "\n")
        if self.output_file:
            if self.output_file_name is None:
                raise Exception('log_type of "file" was chosen, but no log file specified')

            if os.path.exists(self.output_file_name):
                append_write = 'a'  # append if already exists
            else:
                append_write = 'w'  # make a new file if not

            with open(self.output_file_name, append_write) as f:
                f.write(str(data) + '\n')
        if self.output_syslog:
            syslog.openlog(facility=syslog.args_dict['syslog_facility'])
            syslog.syslog(data)
        if self.output_mozdef:
            msg = {}
            msg['timestamp'] = str(datetime.datetime.utcnow())
            msg['hostname'] = socket.getfqdn()
            msg['category'] = ['ldap']
            msg['tags'] = ['ldap']
            msg['summary'] = 'LDAP-Humanizer:{}:{}'.format(data['conn_id'], data['client'])

            resp = requests.post(self.mozdef_url, data=msg)
            if resp.code != "200":
                print("Failed to post to mozdef")
