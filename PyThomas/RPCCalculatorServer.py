import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler




# Restrict to a particular path.
from PyThomas.Calculator import Calculator


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class CalculatorRPCServer:
    # All five basic operators available by default
    def __init__(self, port_no, valid_operators={'+', '-', '*', '/', '^'}):
        # Create server
        self.port_no = port_no
        self.server = SimpleXMLRPCServer(("localhost", port_no), requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.valid_operators = valid_operators

        self.calculator = Calculator()
        self.server.register_function(self.calculate, 'calculate')
        self.server.register_function(self.getinfo, 'info')
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        print("Server initialized on port {0} for operators {1}".format(self.port_no, self.valid_operators))

    def getinfo(self):
        return "Port {0}, valid operators: {1}".format(self.port_no, self.valid_operators)

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