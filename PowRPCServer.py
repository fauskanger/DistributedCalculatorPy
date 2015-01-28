from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class PowRPCServer(SimpleXMLRPCServer):
    kind = 'test'