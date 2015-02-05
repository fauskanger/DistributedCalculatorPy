import threading
import xmlrpc.client
from flask import Flask, jsonify, make_response, abort

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
from Calculator import Calculator


# Base server class
class CalculatorRESTServer:
    # All five basic operators available by default

    def __init__(self, port_no, valid_operators={'+', '-', '*', '/', '^'},
                 domain="localhost", main_server_url='http://localhost:8000', protocol="http://"):

        # Create server
        self.is_closed = False
        self.port_no = port_no
        self.domain = domain
        self.protocol = protocol
        self.address = "{0}{1}:{2}".format(self.protocol, self.domain, self.port_no)

        self.server = Flask(__name__)

        # self.server = SimpleXMLRPCServer((domain, int(port_no)), requestHandler=RequestHandler)
        # self.server.register_introspection_functions()
        self.valid_operators = valid_operators

        # Module to compute problems
        self.calculator = Calculator()

        # Create RPC interface
        # self.server.register_function(self.calculate, 'calculate')
        # self.server.register_function(self.getinfo, 'info')
        # self.server.register_function(self.get_port, 'get_port_no')

        # Connect to main server as RPC-client, so later as a RPC-CalculatorServer
        self.main_server_url = main_server_url
        # self.rpc_main_client = xmlrpc.client.ServerProxy(self.main_server_url)

        # Because starting a server blocks the program, it's done in a separate thread
        self.server_thread = threading.Thread(target=self.server.run(port=self.port_no, debug=True))

        print("Server initialized on port {0} for operators {1}".format(self.port_no, self.valid_operators))

    def get_info(self):
        @self.server.route('/api/info', methods=['GET'])
        def getinfo():
            return "Domain:{2} Port: {0} Valid operators: {1}".format(self.port_no, self.valid_operators, self.domain)

    @self.server.route('/api/port', methods=['GET'])
    def get_port(self):
        return self.port_no

    @self.server.route('/api/calculate', methods=['GET'])
    def calculate(self, x, y, operator):
        print("Server {0} is asked to calculate {1} and {2} with operator {3}"
              .format(self.address, x, y, operator))
        if operator in self.valid_operators:
            # print("Calling calculation method.")
            return self.calculator.calculate(x, y, operator)
        else:
            return "Could not calculate {0} and {1} with operator {2}".format(x, y, operator)

    def start(self):
        self.server_thread.start()
        print("Started {0} ({1})".format(self.address, self.valid_operators))
        self.register_with_main()

    def register_with_main(self):
        # Set up as child to main server if not main server
        if self.main_server_url != "{0}:{1}".format(self.domain, self.port_no):
            # Register each operator:
            for operator in self.valid_operators:
                if not self.rpc_main_client.register_child_server(self.address, operator):
                    print("Server {0} could not register operator {1}.".format(self.address, operator))
