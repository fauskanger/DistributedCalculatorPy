import sys
from PyThomas.DistributedCalculatorServer import DistributedCalculator

dc = DistributedCalculator()

problems = {
    "6+2",
    "6-2",
    "6*2",
    "6/2",
    "6^2",
    "1.0+2",
    "0.5+0.6",
    "1/3",
    "4^0.5",
    "2^0.5",
    "0x10+16"
}

for problem in problems:
    print("-"*10)
    print("Sending problem: {0} to main server (port {1})".format(problem, dc.port_no))
    result = dc.send_problem(problem)
    # print("Answer from main server (port {0}):".format(dc.port_no))
    print("Result: {0} => {1}".format(problem, result))

sys.exit(0)