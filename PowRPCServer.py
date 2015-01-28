from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client

class PowRPCServer(SimpleXMLRPCServer):
    def power(x,y):
        powServer = SimpleXMLRPCServer(("localhost", 8001), requestHandler=SimpleXMLRPCRequestHandler)
        powServer.register_function(pow)

        p = xmlrpc.client.ServerProxy('http://localhost:8000')
        result = p.pow(x,y)

        powServer.server_close()
        return result


#powerOf = getattr(PowRPCServer,PowRPCServer.power(x,))
