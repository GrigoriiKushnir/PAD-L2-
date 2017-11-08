import asyncio
import json
import dicttoxml


# noinspection PyTupleAssignmentBalance
class MyProxy:
    def __init__(self, ip='localhost', port='31337'):
        self.ip = ip
        self.port = port
        self.loop = asyncio.get_event_loop()
        with open("conf.json") as config:
            self.conf = json.load(config)

    @asyncio.coroutine
    def handle_message(self, reader, writer):
        data = []
        message = json.loads((yield from reader.read(1024)).decode('utf-8'))
        sort = message.get("sort")
        print(sort)
        for node in self.conf:
            master = self.conf[node]["master"]
            try:
                if master:
                    ip = self.conf[node]["ip"]
                    port = self.conf[node]["port"]
                    reader_node, writer_node = yield from asyncio.open_connection(
                        ip, port, loop=self.loop
                    )
                    payload = json.dumps({
                        'type': 'command',
                        'command': 'get',
                        "sort": sort
                    }).encode('utf-8')
                    writer_node.write(payload)
                    node_resp = json.loads((yield from reader_node.read(1024)).decode())
                    data += node_resp
                    print(data)
            except Exception as exc:
                print("Could not retrieve data: ", exc)
                pass
        if message.get('xml'):
            xml = dicttoxml.dicttoxml(data, attr_type=False, custom_root="items")
            writer.write(xml)
            yield from writer.drain()
        else:
            writer.write(json.dumps(data).encode())
            yield from writer.drain()

    def start(self):
        coro = asyncio.start_server(self.handle_message, self.ip, self.port, loop=self.loop)
        proxy = self.loop.run_until_complete(coro)
        try:
            print("Proxy started.")
            self.loop.run_forever()
        except Exception as e:
            print("proxy", e)
            pass
        proxy.close()
        self.loop.run_until_complete(proxy.wait_closed())
        self.loop.close()


if __name__ == "__main__":
    proxy = MyProxy()
    proxy.start()
