import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
from CalculatorRESTServer import CalculatorRESTServer
from MainCalculatorRESTServer import MainCalculatorRESTServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class DistributedCalculator():

    def __init__(self):
        # Main server settings
        self.port_no = 8000
        self.main_operators = {'+', '-'}

        # Create and start main server
        self.server_instance = MainCalculatorRESTServer(self.port_no, self.main_operators)
        self.server_instance.start()

        # Create client to main RPC-server
        self.rpc_main_client = xmlrpc.client.ServerProxy('http://localhost:{0}'.format(self.port_no))

        # The child servers, populated below
        self.child_server_instances = []

        # Define operators for child servers
        self.child_server_parameters = {
            8002: {'*', '/'},
            8003: {'^'}
        }

        # Key to list of operators is the port number
        for child_port_no in self.child_server_parameters.keys():
            child_operators = self.child_server_parameters[child_port_no]
            self.child_server_instances.append(CalculatorRESTServer(child_port_no, child_operators))

        # Start child servers
        for child in self.child_server_instances:
            child.start()

    def send_problem(self, expression):
        return self.rpc_main_client.calculate_expression(str(expression))

