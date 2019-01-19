from bitcoin.rpc import RawProxy

p = RawProxy(service_port=18332)
addr = '2N3WJgs4sTMmP3SNJHcY4T7fu3HdDet9oBC'
info = p.getbalance()
print(info)
