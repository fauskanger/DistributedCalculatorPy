import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')
print(s.system.listMethods())

print("2 + 3 = ", s.add(2, 3))
print("5 * 2 = ", s.mul(5, 2))
print("40 / 2 = ", s.divide(40, 2))
print("2 ^ 3 = ", s.pow(2, 3))