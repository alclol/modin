from cloudburst.client.client import CloudburstConnection
local_cloud = CloudburstConnection('127.0.0.1', '127.0.0.1', local=True)

make_list = local_cloud.register(lambda _, i: [x*x for x in range(i)], 'make_list')
list_5 = make_list(5)
take_elem = local_cloud.register(lambda _, l, i: l[i], 'take_elem')
# breakpoint()
res = take_elem(list_5, 3)
print(res)
