import re
from ldap_access_log_humanizer.file_descriptor import FileDescriptor
from ldap_access_log_humanizer.operation import Operation
from ldap_access_log_humanizer.custom_logger import CustomLogger
import datetime


class Connection:
    def __init__(self, conn_id, args_dict):
        self.conn_id = conn_id
        self.time = ""
        self.server = ""
        self.process = ""
        self.operations = {}
        self.tls_status = False
        self.file_descriptors = []
        self.logger = CustomLogger(args_dict)
        self.last_updated = datetime.datetime.now()

    def dict(self):
        return {
            "conn_id": self.conn_id,
            "time": self.time,
            "client": self.client(),
            "server": self.server,
            "tls": self.tls()
        }

    def reconstitute(self, event_dict):
        combined_dict = {}
        combined_dict.update(self.dict())
        combined_dict.update(event_dict)
        return combined_dict

    def tls(self):
        for file_descriptor in self.file_descriptors:
            if file_descriptor.verb == "TLS" and file_descriptor.details.startswith("established"):
                self.tls_status = True

        return self.tls_status

    def closed(self):
        for file_descriptor in self.file_descriptors:
            if file_descriptor.verb == "closed":
                return True

        return False

    def client(self):
        for file_descriptor in self.file_descriptors:
            if file_descriptor.verb == "ACCEPT":
                pattern = r'from IP=(\d+\.\d+\.\d+\.\d+):'
                match = re.search(pattern, file_descriptor.details)
                if match:
                    return match.group(1)

        return ""

    def add_operation(self, rest):
        # Expecting something like:
        # op=1 BIND dn="uid=bind-generateusers,ou=logins,dc=example" mech=SIMPLE ssf=0
        #
        pattern = r'^op=(\d+) (.*)$'
        match = re.search(pattern, rest)

        if match:
            op_id = match.group(1)
            operation = self.operations.get(int(op_id))

            # if an existing operation, update it's context
            if operation:
                operation.add_event(match.group(2))
            # if a new operation, add it to our operations list
            else:
                operation = Operation(int(op_id))
                operation.add_event(match.group(2))
                self.operations[int(op_id)] = operation

            if operation.loggable():
                self.logger.log(self.reconstitute(operation.dict()))
        else:
            raise Exception('Malformed operation: {}'.format(rest))

    def add_file_descriptor(self, rest):
        # Expecting something like:
        # fd=34 ACCEPT from IP=192.168.1.1:56822 (IP=0.0.0.0:389)
        #
        pattern = r'^fd=(\d+) (.*)$'
        match = re.search(pattern, rest)

        if match:
            file_descriptor = FileDescriptor(int(match.group(1)))
            file_descriptor.add_event(match.group(2))
            self.file_descriptors.append(file_descriptor)

            if file_descriptor.loggable():
                self.logger.log(self.reconstitute(file_descriptor.dict()))
        else:
            raise Exception('Malformed file file_descriptor: {}'.format(rest))

    # Something happened, this method's job is to update the context
    def add_event(self, event):
        self.time = event['time']
        self.server = event['server']
        self.process = event['process']
        self.add_rest(event['rest'])
        self.last_updated = datetime.datetime.now()

    def add_rest(self, rest):
        if rest.startswith('op'):
            self.add_operation(rest)
        elif rest.startswith('fd'):
            self.add_file_descriptor(rest)
        else:
            raise Exception('Unsupported option: {}'.format(rest))
