import os
import sys


class CustomLogger:
    def __init__(self, log_type='stdout', output_file=None):
        self.log_type = log_type or 'stdout'
        self.output_file = output_file
        if log_type == 'syslog':
            self.syslog_port = args.get('syslog_port')

    def log(self, data):
        if self.log_type == "stdout":
            print(str(data))
        elif self.log_type == 'syslog':
            pass
        elif self.log_type == "stderr":
            sys.stderr.write(str(data) + "\n")
        elif self.log_type == "file":
            if self.output_file == None:
                raise Exception('log_type of "file" was chosen, but no log file specified')

            if os.path.exists(self.output_file):
                append_write = 'a'  # append if already exists
            else:
                append_write = 'w'  # make a new file if not

            with open(self.output_file, append_write) as f:
                f.write(str(data) + '\n')
