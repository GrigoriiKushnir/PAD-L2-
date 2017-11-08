import socket
import json
from xml.dom.minidom import parseString
from lxml import etree
from jsonschema import validate, Draft4Validator

schema = {
    "type": "array",
    "$schema": "http://json-schema.org/schema#",
    "items": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "default": "",
            },
            "age": {
                "type": "integer",
                "default": 0,
            }
        }
    }
}

Draft4Validator.check_schema(schema)


class MyClient:
    def __init__(self, xml, sort=None, proxy_port=31337, proxy_ip='localhost'):
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.xml = xml
        self.sort = sort

    def get_info(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.proxy_ip, self.proxy_port))
        payload = json.dumps({
            'type': 'command',
            'command': 'get',
            'xml': self.xml,
            'sort': self.sort
        }).encode('utf-8')
        conn.send(payload)
        data = conn.recv(1024)
        conn.close()
        return data.decode('utf-8')


if __name__ == "__main__":
    xml_bool = True
    client = MyClient(xml=xml_bool, sort='-age')
    info = client.get_info()
    print(info)

    if xml_bool:
        dom = parseString(info)
        print(dom.toprettyxml())
        with open("f.xml", "wb") as f:
            f.write(info.encode())
        xml_name = "f.xml"
        doc = etree.parse(xml_name)
        relaxng_doc = etree.parse("ng_schema")
        relaxng = etree.RelaxNG(relaxng_doc)

        print(relaxng.validate(doc))
        relaxng.assertValid(doc)
    else:
        validate(json.loads(info), schema)
