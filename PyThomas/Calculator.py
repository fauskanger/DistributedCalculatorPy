class Calculator:
    def __init__(self):
        self.maths = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            '^': self.power
        }

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def subtract(x, y):
        return x - y

    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def divide(x, y):
        if y != 0:
            return x / y
        else:
            # raise ZeroDivisionError
            return "Cannot divide by Zero!"

    @staticmethod
    def power(base, power):
        return pow(base, power)

    def calculate(self, x, y, operator):
        if operator in self.maths:
            return self.maths[operator](float(x), float(y))
