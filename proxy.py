import asyncio


class MyProxy:
    def __init__(self, ip='localhost', port='1337'):
        self.ip = ip
        self.port = port
        self.loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def handle_message(self, reader, writer):
        data = yield from reader.read(1024)
        writer.write("Your data.".encode())
        yield from writer.drain()
        print(data.decode('utf-8'))

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
