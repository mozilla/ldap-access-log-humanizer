import re


class Connection:
    def __init__(self, conn_id):
        self.conn_id = conn_id
        self.tls = False
        self.client = ""
        self.time = ""
        self.fd = ""
        self.op = ""
        self.verb = ""
        self.verb_details = ""

    def log(self):
        return {"conn_id": self.conn_id,
                "tls": self.tls,
                "client": self.client,
                "time": self.time,
                "fd": self.fd,
                "op": self.op,
                "verb": self.verb,
                "verb_details": self.verb_details}

    # Something happened, this method's job is to update the context
    def add_event(self, event):
        self.time = event['time']
        self.server = event['server']
        self.process = event['process']
        self.add_rest(event['rest'])

    def add_accept(self, verb_details):
       # Example: from IP=192.168.1.1:56822 (IP=0.0.0.0:389)
        pattern = r'^from IP=(\d+\.\d+\.\d+\.\d+)'
        match = re.search(pattern, verb_details)

        if match:
            self.client = match[1]
        else:
            raise Exception('Failed to parse: {}'.format(verb_details))

    def add_tls(self, verb_details):
        if verb_details.startswith('established'):
            self.tls = True

    def add_rest(self, rest):
        self.fd = ""
        self.op = ""
        self.verb = ""
        self.verb_details = ""

        # Example: fd=34 ACCEPT ...
        pattern = r'^(\w+)=(\d+) (\w+)\s?(.*)$'
        match = re.search(pattern, rest)

        if match:
            if match[1] == 'fd':
                self.fd = int(match[2])
            elif match[1] == 'op':
                self.op = int(match[2])
            else:
                raise Exception('Unsupported option: {}'.format(match[1]))

            self.verb = match[3]
            self.verb_details = match[4]

            # Some verbs have a special impact on a connection, so
            # we handle those here to update that context.
            if self.verb == "ACCEPT":
                self.add_accept(self.verb_details)
            elif self.verb == "TLS":
                self.add_tls(self.verb_details)

        else:
            raise Exception('Failed to parse: {}'.format(rest))
