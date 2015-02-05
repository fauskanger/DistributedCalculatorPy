import xmlrpc.client
from PyThomas.CalculatorRPCServer import CalculatorRPCServer


# Main server class, derived from CalculatorRPCServer
class MainCalculatorRPCServer(CalculatorRPCServer):
    def __init__(self, port_no, self_operators, always_override_operators=True):
        super().__init__(port_no, self_operators)

        # Maps operators to clients of child servers as operator=>server, populated below
        self.calculator_client_dictionary = dict()
        # RPC-servers to which main is a client
        self.rcp_child_clients = dict()

        # Map operators to main server (self)
        # NB! IT SHOULD BE NOTED that self is not same type as clients,
        # so this is checked for in self.calculate_expression.
        self.self_operators = self_operators
        self.always_override_operators = always_override_operators
        self.register_self_operators()

        # Create RPC-interface for user input
        self.server.register_function(self.calculate_expression)
        # Create RPC-interface for child servers to register themselves
        self.server.register_function(self.register_child_server)
        print("Main server initialized.")

    @staticmethod
    def split_expression(expression):
        ex = str(expression)
        for operator in {"+", "-", "*", "/", "^"}:
            operator_index = ex.find(operator)
            if operator_index < 0:
                continue
            left = ex[:operator_index]
            right = ex[operator_index + 1:]
            try:
                left = float(left)
                right = float(right)
                return [left, operator, right]
            except ValueError:
                return "Left: {0} or Right: {1} or both is not a number.".format(left, right)
        return "Could not parse expression into two parts"

    # Method revealed by RPC for user input to the calculator.
    def calculate_expression(self, expression):
        # Strip whitespace:
        expression = str(expression).strip()
        print("Main server receive problem to solve: {0}".format(expression))
        # Parse into parts left, right and operator:
        parts = self.split_expression(expression)
        if len(parts) != 3:
            return "Incorrect number of parts in expression, must be 3; two decimals and a valid operator."

        operator = parts[1]
        left = parts[0]
        right = parts[2]

        if operator in self.calculator_client_dictionary.keys():
            calc_client = self.calculator_client_dictionary[operator]
            if calc_client == self:
                print("Selected client: {0}".format(calc_client.getinfo()))
                print("Calculating locally on main server.")
                return self.calculate(left, right, operator)
            print("Selected client: {0}".format(self.calculator_client_dictionary[operator].info()))
            return self.calculator_client_dictionary[operator].calculate(left, right, operator)

        return 'Expression is not two decimals and a valid operator:'

    # Method revealed by RPC for other servers to register themselves as
    def register_child_server(self, child_domain, child_operator):
        if child_domain == self.port_no:
            return False
        print("Main server received registration from child server ({0}) with operator: {1}"
              .format(child_domain, child_operator))

        # child_domain = int(child_domain)

        # Add new clients
        if child_domain not in self.rcp_child_clients.keys():
            # Connect as client to child RPC-server
            self.rcp_child_clients[child_domain] \
                = xmlrpc.client.ServerProxy(str(child_domain))

        # Map operator to server
        self.calculator_client_dictionary[child_operator] = self.rcp_child_clients[child_domain]

        # Some clients may have registered with same operators
        if self.always_override_operators:
            self.register_self_operators()
        return True

    def say_hello(self):
        return "{0}, here. Hello!".format(self.port_no)

    # Used to overwrite any other servers' operators
    # if overlapping with self.self_operators.
    def register_self_operators(self):
        for operator in self.self_operators:
            self.calculator_client_dictionary[operator] = self
