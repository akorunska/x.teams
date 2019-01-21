from bitcoin.rpc import RawProxy

p = RawProxy(service_port=18332)
info = p.getbalance()
print(info)
