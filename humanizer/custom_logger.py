import os
import sys
import mozdef_client


class CustomLogger:
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
            if self.output_file_name == None:
                raise Exception('log_type of "file" was chosen, but no log file specified')

            if os.path.exists(self.output_file_name):
                append_write = 'a'  # append if already exists
            else:
                append_write = 'w'  # make a new file if not

            with open(self.output_file_name, append_write) as f:
                f.write(str(data) + '\n')
        elif self.output_mozdef or self.output_syslog:
            msg = mozdef_client.MozDefEvent(self.mozdef_url)
            msg.summary = 'LDAP-Humanizer:{}:{}'.format(data['conn_id'], data['client'])
            msg.tags = ['ldap']
            # make sure it's a dict
            msg.details = data
            msg.categories = ['ldap']
            if self.output_syslog:
                if not self.output_mozdef:
                    msg.set_send_to_syslog(True, only_syslog=True)
                else:
                    msg.set_send_to_syslog(True)
            msg.send()

