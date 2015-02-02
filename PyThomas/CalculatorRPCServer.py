import threading
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
from PyThomas.Calculator import Calculator


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class CalculatorRPCServer:
    # All five basic operators available by default
    def __init__(self, port_no, valid_operators={'+', '-', '*', '/', '^'}, main_server_port_no=8000):

        # Create server
        self.is_closed = False
        self.port_no = port_no
        self.server = SimpleXMLRPCServer(("localhost", int(port_no)), requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.valid_operators = valid_operators

        # Module to compute problems
        self.calculator = Calculator()

        # Create RPC interface
        self.server.register_function(self.calculate, 'calculate')
        self.server.register_function(self.getinfo, 'info')
        self.server.register_function(self.get_port, 'get_port_no')
        # self.server.register_function(self.server_close)

        # Connect to main server as RPC-client, so later as a RPC-CalculatorServer
        self.main_server_port_no = main_server_port_no
        self.rpc_main_client = xmlrpc.client.ServerProxy('http://localhost:' + str(self.main_server_port_no))

        # Because starting a server blocks the program, it's done in a separate thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        print("Server initialized on port {0} for operators {1}".format(self.port_no, self.valid_operators))

    def getinfo(self):
        return "Port {0}, valid operators: {1}".format(self.port_no, self.valid_operators)

    def get_port(self):
        return self.port_no

    def calculate(self, x, y, operator):
        print("Server on port {0} is asked to calculate {1} and {2} with operator {3}"
              .format(self.port_no, x, y, operator))
        if operator in self.valid_operators:
            # print("Calling calculation method.")
            return self.calculator.calculate(x, y, operator)
        else:
            return "Could not calculate {0} and {1} with operator {2}".format(x, y, operator)

    def start(self):
        self.server_thread.start()
        print("Started port {0} ({1})".format(self.port_no, self.valid_operators))
        self.register_with_main()

    def register_with_main(self):
        # Set up as child to main server if not main server
        if self.main_server_port_no != self.port_no:
            # Register each operator:
            for operator in self.valid_operators:
                if not self.rpc_main_client.register_child_server(self.port_no, operator):
                    print("Server on port {0} could not register operator {1}.".format(self.port_no, operator))

    # def server_close(self):
    #     if self.is_closed:
    #         return False
    #     self.server.server_close()
    #     return True