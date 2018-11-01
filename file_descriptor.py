class FileDescriptor:
    def __init__(self, fd_id):
        self.fd_id = fd_id
        self.verb = ""
        self.details = ""

    def add_event(self, rest):
        tokenized_rest = rest.split(" ")
        self.verb = tokenized_rest[0]
        self.details = ' '.join(tokenized_rest[1:])

    def dict(self):
        return {
            "fd_id": self.fd_id,
            "verb": self.verb,
            "details": self.details
        }

    def loggable(self):
        # We always want to log fd
        return True
