import asyncio
import json
from multiprocessing import Process
from operator import itemgetter

data_dict = {
    "n1": [{"name": "aa", "age": 11}, {"name": "bb", "age": 12}],
    "n2": [{"name": "cc", "age": 21}, {"name": "dd", "age": 22}],
    "n3": [{"name": "ee", "age": 31}, {"name": "ff", "age": 32}],
    "n4": [{"name": "gg", "age": 41}, {"name": "hh", "age": 42}],
    "n5": [{"name": "ii", "age": 51}, {"name": "jj", "age": 52}],
    "n6": [{"name": "kk", "age": 61}, {"name": "ll", "age": 62}],
    "n7": [{"name": "mm", "age": 71}, {"name": "nn", "age": 72}]
}


class MyNode:
    def __init__(self, master, port, ip='localhost', slaves=None):
        self.ip = ip
        self.port = port
        self.slaves = slaves
        self.master = master
        self.loop = asyncio.get_event_loop()
        self.node_nr = "n" + str(self.port % 10)
        with open("conf.json") as config:
            self.conf = json.load(config)

    def sort_data(self, sort_field):
        sort_desc = True if "-" in sort_field else False
        sort_key = sort_field if "-" not in sort_field else sort_field[1:]
        return sorted(data_dict[self.node_nr], key=itemgetter(sort_key), reverse=sort_desc)

    def filter_data(self, data, filt):
        field = filt["field"]
        op = filt["op"]
        val = filt["val"]
        resp = []
        for d in data:
            op_func = getattr(d[field], op)
            if op_func(val):
                resp.append(d)
        return resp

    def data_edit(self, data, sort, filt):
        if sort:
            data += self.sort_data(sort)
        if filt:
            data = self.filter_data(data, filt)
        if sort is None and filt is None:
            data = data_dict[self.node_nr]
        return data

    @asyncio.coroutine
    def handle_message(self, reader, writer):
        message = json.loads((yield from reader.read(1024)).decode('utf-8'))
        sort = message.get("sort")
        filt = message.get("filter")
        if self.master:
            data = []
            data = self.data_edit(data, sort, filt)
            slaves = self.conf[self.node_nr]["slaves"]
            for n in slaves:
                payload = json.dumps({
                    'type': 'command',
                    'command': 'get',
                    'sort': sort,
                    'filter': filt
                }).encode('utf-8')
                ip = self.conf[n]["ip"]
                port = self.conf[n]["port"]
                reader_node, writer_node = yield from asyncio.open_connection(
                    ip, port, loop=self.loop
                )
                writer_node.write(payload)
                node_resp = yield from reader_node.read(1024)
                data += json.loads(node_resp.decode()).get('payload')
            writer.write(json.dumps(data).encode())
            yield from writer.drain()
        else:
            pl = []
            pl = self.data_edit(pl, sort, filt)
            payload = json.dumps({
                'type': 'response',
                'payload': pl,
            }).encode('utf-8')
            writer.write(payload)
            yield from writer.drain()

    def start(self):
        coro = asyncio.start_server(self.handle_message, self.ip, self.port, loop=self.loop)
        proxy = self.loop.run_until_complete(coro)
        try:
            print("Node", self.node_nr)
            self.loop.run_forever()
        except Exception as e:
            print("proxy", e)
            pass
        proxy.close()
        self.loop.run_until_complete(proxy.wait_closed())
        self.loop.close()


def start_node(master, port):
    node = MyNode(master=master, port=port)
    node.start()


if __name__ == "__main__":
    p2 = Process(target=start_node, args=(True, 31102))
    p3 = Process(target=start_node, args=(False, 31103))
    p6 = Process(target=start_node, args=(True, 31106))
    p7 = Process(target=start_node, args=(False, 31107))

    p2.start()
    p3.start()
    p6.start()
    p7.start()
