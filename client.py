import socket
import json

import xml.etree.ElementTree as ET


class MyClient:
    def __init__(self, xml, proxy_port=31337, proxy_ip='localhost'):
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.xml = xml

    def get_info(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.proxy_ip, self.proxy_port))
        payload = json.dumps({
            'type': 'command',
            'command': 'get',
            'xml': self.xml
        }).encode('utf-8')
        conn.send(payload)
        data = conn.recv(1024)
        conn.close()
        return data.decode('utf-8')


if __name__ == "__main__":
    client = MyClient(xml=True)
    info = client.get_info()
    print(info)
    # print(info)
    # xml = dicttoxml.dicttoxml(info, attr_type=False)
    # print(xml)
    # with open("f.xml", "wb") as f:
    #     f.write(xml)
        # tree = ET.parse("f.xml")
        # root = tree.getroot()
        # print(root.tag)
