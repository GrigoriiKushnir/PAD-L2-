#### Installation
To run this project you need Python>=3.5 (recommended 3.6).
[How to install it?](https://www.python.org/downloads/)

Pip (python package manager) should be installed with Python >= 3.5. However,
if you can't find it, check out [this page](https://pip.pypa.io/en/stable/installing/).

#### Dependencies

This project uses jsonschema, lxml and dicttoxml libraries.
The dependencies is stated in: `./requirements/local.txt`.
Just execute
`pip install -r requirements/local.txt`

#### Running project

This project has 3 components:
- Proxy;
- Node;
- Client;

Proxy (`src/proxy.py`) listens on `localhost:31337` for requests from clients.

Node (`src/node.py`) listens on a port taken given by user.
Reads from 'files/config.json' it's `master` and `slaves` parameters.
Slaves return their data to any who asks them and edit it if needed based on request (filter/sort), see more in
`docs/protocol-specs.md`.
Masters edit their data if needed and request data from slaves. After parsing their slaves they return the data
to proxy.

Client requests data from Proxy. Client can specify the format they want the data to be returned, XML or JSON. Client
validates the data using RELAXNG for XML ('files/ng_schema') or JSONschema for JSON ('files/schema.json').

See protocol-specs for more info about client-proxy-nodes communication.

To run the proxy just execute the `src/proxy.py` file

`python3.5 src/proxy.py`

To start node and respectively client run

`python3.5 src/node.py`

and

`python3.5 src/client.py`

Those files should be run from separated terminals.

*Note: Instead of `python3.5` you could try to use `python3.4` if you have it.*