try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

class SyslogServer(SocketServer.BaseRequestHandler):
    def __init__(self, fp, args_dict):
        self.args_dict = args_dict
        if self.args_dict['host']:
            self.host = self.args_dict['host']
        if self.args_dict['port']:
            self.port = self.args_dict['port']
        self.logger = CustomLogger(self.args_dict)

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        parser = Parser(fp, args_dict)
        parser.parse_line()

    def serve(self):
        server = SocketServer.UDPServer((self.host,self.port), self.handle())
        server.serve_forever(poll_interval=0.5)

    def start_syslog(self):
        if self.args_dict['daemonize'] == True:
            import daemon
            from daemon import pidfile
            pidf='/tmp/humanizer.pid'
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
            self.serve()
