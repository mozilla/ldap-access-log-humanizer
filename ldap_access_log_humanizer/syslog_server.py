try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
from ldap_access_log_humanizer.custom_logger import CustomLogger
from ldap_access_log_humanizer.parser import Parser

syslog_server_parser = None


class SyslogUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        # openldap logs to local4 facility, which prepends a debug code of <167>
        data = data.lstrip('<167>')
        socket = self.request[1]
        global syslog_server_parser
        syslog_server_parser.parse_line(str(data))


class UDPServer(SocketServer.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, args_dict, bind_and_activate=True):
        SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass)
        self.args_dict = args_dict


class SyslogServer():

    def __init__(self, args_dict):
        self.args_dict = args_dict
        if self.args_dict['host']:
            self.host = self.args_dict['host']
        if self.args_dict['port']:
            self.port = self.args_dict['port']
        self.logger = CustomLogger(self.args_dict)

        # Override a parser with appropriate args_dict optioned instance
        global syslog_server_parser
        syslog_server_parser = Parser(None, self.args_dict)

    def serve(self):
        server = UDPServer((self.host, int(self.port)), SyslogUDPHandler, self.args_dict)
        server.serve_forever(poll_interval=0.5)

    def start_syslog(self):
        # mostly for testing, we can start a standalone daemon
        if self.args_dict['daemonize']:
            import daemon
            from daemon import pidfile
            pidf = '/tmp/humanizer.pid'
            wdir = os.path.dirname(os.path.abspath(__file__))
            out = self.logger
            with daemon.DaemonContext(
                    working_directory=wdir,
                    stdout=out,
                    stderr=out,
                    umask=0o002,
                    pidfile=pidfile.TimeoutPIDLockFile(pidf),
            ) as context:
                self.serve()
        else:
            # when running under systemd, we don't need daemonize, just start serving
            self.serve()
