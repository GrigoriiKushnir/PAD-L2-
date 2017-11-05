import asyncio
import json

data_dict = {
    "n1": [11, 12, 13, 14, 15],
    "n2": [21, 22, 23, 24, 25],
    "n3": [31, 32, 33, 34, 35],
    "n4": [41, 42, 43, 44, 45],
    "n5": [51, 52, 53, 54, 55],
    "n6": [61, 62, 63, 64, 65],
    "n7": [71, 72, 73, 74, 75]
}


class MyNode:
    def __init__(self, master, slaves, port, ip='localhost'):
        self.ip = ip
        self.port = port
        self.slaves = slaves
        self.master = master
        self.loop = asyncio.get_event_loop()
        self.node_nr = "n" + str(self.port % 10)
        with open("conf.json") as config:
            self.conf = json.load(config)

    @asyncio.coroutine
    def handle_message(self, reader, writer):
        if self.master:
            data = {self.node_nr: data_dict[self.node_nr]}
            slaves = self.conf[self.node_nr]["slaves"]
            for n in slaves:
                payload = json.dumps({
                    'type': 'command',
                    'command': 'get',
                }).encode('utf-8')
                ip = self.conf[n]["ip"]
                port = self.conf[n]["port"]
                reader_node, writer_node = yield from asyncio.open_connection(
                    ip, port, loop=self.loop
                )
                writer_node.write(payload)
                node_resp = yield from reader_node.read(1024)
                data[n] = json.loads(node_resp.decode()).get('payload')
            print(data)
            writer.write(json.dumps(data).encode())
            yield from writer.drain()
        else:
            message = data_dict[self.node_nr]
            print(message)
            payload = json.dumps({
                'type': 'response',
                'payload': message,
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

if __name__ == "__main__":
    node = MyNode(master=True, slaves=None, port=31102)
    #node = MyNode(master=False, slaves=None, port=31103)
    #node = MyNode(master=True, slaves=None, port=31106)
    #node = MyNode(master=False, slaves=None, port=31107)
    node.start()
