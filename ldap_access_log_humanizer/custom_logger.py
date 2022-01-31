import datetime
import json
import os
import requests
import socket
import sys
import syslog


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
        self.syslog_facility = args_dict['syslog_facility']
        self.syslog_map = {
            'LOG_KERN': 0,
            'LOG_USER': 8,
            'LOG_MAIL': 16,
            'LOG_DAEMON': 24,
            'LOG_AUTH': 32,
            'LOG_LRP': 48,
            'LOG_NEWS': 56,
            'LOG_UUCP': 64,
            'LOG_CRON': 72,
            'LOG_LOCAL0': 128,
            'LOG_LOCAL1': 136,
            'LOG_LOCAL2': 144,
            'LOG_LOCAL3': 152,
            'LOG_LOCAL4': 160,
            'LOG_LOCAL5': 168,
            'LOG_LOCAL6': 176,
            'LOG_LOCAL7': 184,
        }

    def log(self, data, error=False):
        if error:
            print(data)
        else:
            if self.output_stdout:
                print(json.dumps(data))
            if self.output_stderr:
                sys.stderr.write(json.dumps(data) + "\n")
            if self.output_file:
                if self.output_file_name is None or self.output_file_name == "":
                    raise Exception('log_type of "file" was chosen, but no log file specified')

                if os.path.exists(self.output_file_name):
                    append_write = 'a'  # append if already exists
                else:
                    append_write = 'w'  # make a new file if not

                with open(self.output_file_name, append_write) as f:
                    f.write(json.dumps(data) + '\n')
            if self.output_syslog:
                facility = self.syslog_map[self.syslog_facility]
                syslog.openlog(facility=facility)
                syslog.syslog(json.dumps(data))
            if self.output_mozdef:
                headers = {
                    'Content-type': 'application/json',
                }
                msg = {}
                msg['timestamp'] = datetime.datetime.utcnow().isoformat()
                msg['hostname'] = socket.getfqdn()
                msg['category'] = 'ldap'
                msg['tags'] = ['ldap']
                msg['summary'] = 'LDAP-Humanizer:{}:{}'.format(data['conn_id'], data['client'])
                msg['details'] = data

                resp = requests.post(self.mozdef_url, headers=headers,  data=json.dumps(msg))
                if not resp.ok:
                    print("Failed to post to mozdef")
