from PyThomas.DistributedCalculatorServer import DistributedCalculator


def test_distributed_calc(dc):
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


def query_user():
    return input("Please enter a math problem: (Exit with 0)")

#
#   MAIN program:
#
def program():
    test = False
    dc = DistributedCalculator()

    if test:
        test_distributed_calc(dc)

    for i in range(1, 3):
        print("-"*5)

    user_input = query_user()
    while user_input != "0":
        result = dc.send_problem(user_input)
        print("Result: {0} => {1}".format(user_input, result))
        print("-"*10)
        user_input = query_user()

    print("Bye bye! Thanks for using awesome distributed calculator.")


#
#   Start script:
#
program()
