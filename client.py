import socket
import time


class MyClient:
    def __init__(self, proxy_port=1337, proxy_ip='localhost'):
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port

    def get_info(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.proxy_ip, self.proxy_port))
        conn.send("Give me data!".encode())
        data = conn.recv(1024)
        conn.close()
        return data.decode('utf-8')


if __name__ == "__main__":
    client = MyClient()
    while True:
        info = client.get_info()
        print(info)
        time.sleep(1)
