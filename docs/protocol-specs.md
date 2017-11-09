## Description of the protocol

The protocol for the system is based on JSON.

`type` is the type of the message. It must be one of the following:
- `command` - perform a command;
- `response` - response message;

`command` is the type of action to be executed by the proxy or the node that receives the message.

The current version exposes only one command:
- `get` - requests data;

`xml` - boolean field, the format of data requested by client. The conversion to needed format is performed on proxy;
- `True` - request XML format;
- `False` - request JSON format;

`sort` is the data sorting field that is performed on node;
- `-field` - sorts the data descending by the field;
- `field` - sorts the data ascending by the field;

`filter` is the filtering field, it is a dict containing following keys:
- `field` - field to be filtered;
- `op` - filtering option;
- `val` - filtering value;

Examples of the structure for the command messages (dicts dumped to json):
```json
{
    "type": "command",
    "command": "get",
    "xml": true,
    "sort": "-age",
    "filter": {
       "field": "name",
       "op": "startswith",
       "val": "n"
    }
}
```
```json
{
    "type": "command",
    "command": "get",
    "xml": false,
    "sort": "-name",
    "filter": {
       "field": "age",
       "op": "__ge__",
       "val": "71"
    }
}
```
```json
{
    "type": "command",
    "command": "get",
    "sort": "-name",
    "filter": {
       "field": "age",
       "op": "__ge__",
       "val": "71"
    }
}
```

Examples of the structure for response messages:
```json
{
    "type": "response",
    "payload": "<data>"
}
```

`payload` is payload of sent/received message.
