import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler




# Restrict to a particular path.
from PyThomas.MainCalculatorRPCServer import MainCalculatorRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Main server, with CalculatorRPCServer as base class
class DistributedCalculator():

    def __init__(self):
        # Main server settings
        self.port_no = 8000
        self.main_operators = {'+', '-'}

        # Define operators for child servers
        self.child_server_operators = {
            8002: {'*', '/'},
            8003: {'^'}
        }
        self.server_instance = MainCalculatorRPCServer(self.port_no, self.main_operators, self.child_server_operators)
        self.server_instance.start()
        self.rpc_client = xmlrpc.client.ServerProxy('http://localhost:{0}'.format(self.port_no))

    def send_problem(self, expression):
        return self.server_instance.calculate_expression(str(expression))