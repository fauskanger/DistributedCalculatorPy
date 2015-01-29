import xmlrpc.client
import itertools

from PyThomas.CalculatorRPCServer import CalculatorRPCServer


class MainCalculatorRPCServer(CalculatorRPCServer):
    def __init__(self, port_no, self_operators, child_server_info):
        super().__init__(port_no, self_operators)

        # The child servers, populated below
        self.child_server_instances = []

        # Maps operators to clients of child servers as operator=>server, populated below
        self.child_dictionary = dict()

        # Key to list of operators is the port number
        for child_port_no in child_server_info.keys():
            child_operators = child_server_info[child_port_no]
            self.child_server_instances.append(CalculatorRPCServer(child_port_no, child_operators))

            # Map operators to servers
            for operator in child_operators:
                self.child_dictionary[operator] = xmlrpc.client.ServerProxy('http://localhost:' + str(child_port_no))

        # Map operators to main server (self)
        # NB! IT SHOULD BE NOTED that self is not same type as clients,
        # so this is checked for in calculation_evaluation.
        for operator in self_operators:
            self.child_dictionary[operator] = self

        # Start servers
        for child in self.child_server_instances:
            child.start()

        # Create RPC-interface for input
        self.server.register_function(self.calculate_expression)
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

    # Method revealed by RPC to users of the calculator.
    def calculate_expression(self, expression):
        print("Main server receive problem to solve: {0}".format(expression))
        parts = self.split_expression(expression)
        if len(parts) != 3:
            parts_print = ""
            comma = ""
            for part in parts:
                parts_print += comma + part
                comma = ", "
            print("Split up expression: {0}".format(parts_print))
            return "Incorrect number of parts in expression, must be 3; two decimals and a valid operator."

        operator = parts[1]
        left = parts[0]
        right = parts[2]

        if operator in self.child_dictionary.keys():
            calc_client = self.child_dictionary[operator]
            if calc_client == self:
                print("Selected client: {0}".format(calc_client.getinfo()))
                print("Calculating locally on main server.")
                return self.calculate(left, right, operator)
            print("Selected client: {0}".format(self.child_dictionary[operator].info()))
            return self.child_dictionary[operator].calculate(left, right, operator)

        return 'Expression is not two decimals and a valid operator:'