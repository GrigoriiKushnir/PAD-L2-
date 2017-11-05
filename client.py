import socket
import json
from xml.dom.minidom import parseString
from lxml import etree
from xml.etree import ElementTree
from io import StringIO


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
    dom = parseString(info)
    # print(dom.toprettyxml())
    with open("f.xml", "wb") as f:
        f.write(info.encode())

    # relaxng_doc = etree.parse("ng_schema")
    # relaxng = etree.RelaxNG(relaxng_doc)

    # xmlschema_doc = etree.parse("f.xsd")
    # xmlschema = etree.XMLSchema(xmlschema_doc)

    dtd = etree.DTD("dtd")

    xml_name = "f.xml"
    doc = etree.parse(xml_name)

    dtd.assertValid(xml_name)
    # relaxng.assertValid(doc)
    # xmlschema.assertValid(doc)
