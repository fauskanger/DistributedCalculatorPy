from math import gamma
from math import factorial


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
    def divide(numerator, denominator):
        if denominator != 0:
            return numerator / denominator
        else:
            # raise ZeroDivisionError
            return "Cannot divide by Zero!"

    @staticmethod
    def power(base, power):
        return pow(base, power)

    @staticmethod
    def factorial(x):
        if int(x) == x:
            return factorial(x)
        else:
            return gamma(x)

    def calculate(self, x, y, operator):
        if operator in self.maths:
            return self.maths[operator](float(x), float(y))
        else:
            return "Cannot compute. {0} is not recognized as operator or symbol.".format(operator)
