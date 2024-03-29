from statistics import mean
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import xmlrpc.client


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ServerThread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.localServer = SimpleXMLRPCServer(("localhost", port), requestHandler=RequestHandler)
        self.localServer.register_introspection_functions()

    def run(self):
        self.localServer.serve_forever()

main = ServerThread(8000)
s1 = ServerThread(8001)
s2 = ServerThread(8002)

# S1-functions
class S1Funcs:

    def mul(self, x, y):
        return x * y

    def divide(self, x, y):
        if y != 0:
            return x / y
        else:
            return ZeroDivisionError

s1.localServer.register_instance(S1Funcs())
s1.start()

s2.localServer.register_function(pow)
s2.start()

# Client proxies from Main to S1 and S2
c1 = xmlrpc.client.ServerProxy('http://localhost:8001')
c2 = xmlrpc.client.ServerProxy('http://localhost:8002')

# Main-server functions.
class MainFuncs:
   
    def add(self, x, y):
        return x + y
    def sub(self, x, y):
        return x - y

    # Pass on to S1-proxy
    def divide(self, x, y):
        return c1.divide(x, y)
    def mul(self, x, y):
        return c1.mul(x, y)

    # Pass on to S2-proxy
    def pow(self, x, y):
        return c2.pow(x, y)


main.localServer.register_instance(MainFuncs())
main.start()
