# python-idmefv2

A Python library for parsing, handling, and generating JSON IDMEFv2 messages.

It can be used to represent Incident Detection Message Exchange Format (IDMEFv2) messages in memory, validate them and serialize/unserialize them for exchange with other systems.

This code is currently in an experimental status and is regularly kept in sync with the development status of the IDMEFv2 format, as part of the [IDMEFv2 Task Force project](https://www.idmefv2.org/).

The latest revision of the IDMEFv2 format specification can be found in the [idmefv2-definition repository](https://github.com/IDMEFv2/idmefv2-Specification).

IDMEFv2 messages can be transported using the [python-idmefv2-transport](https://github.com/IDMEFv2/python-idmefv2-transport) Python library.

You can find more information about the previous version (v1) of the Intrusion Detection Message Exchange Format in [RFC 4765](https://tools.ietf.org/html/rfc4765).

## Prerequisites

The following prerequisites must be installed on your system to install and use this library:

- Python 3.10 or later
- The Python [setuptools](https://pypi.org/project/setuptools/) package (usually available as a system package under the name `python3-setuptools`)

Library dependencies are:
- The Python [jsonschema](https://pypi.org/project/jsonschema/) package

## Installation

### Installation from sources

This repository uses Git submodules to include a copy of the IDMEFv2 JSON schema. When installing from sources using a Git clone, make sure you also initialize the submodules:

``` sh
git submodule init
```

It is highly recommended to install the library in a Python *virtualenv* https://virtualenv.pypa.io/en/latest/, unless running inside a container.

Installing the dependencies using `requirements.txt` is not supported; this repository provides a `pyproject.toml` which is the recommended alternative.

To install the library, simply run in the root directory of the git clone:

``` sh
. /PATH/TO/THE/PIP/OF/YOUR/VIRTUALENV/bin/activate  # only if using a virtualenv
pip install --editable .
```

This will install as well the dependencies.

### Installation from packages

`python-idmefv2` provides packages currently hosted on [TestPyPI](https://test.pypi.org/).

To install using TestPyPI, use the following command:

```
pip install --extra-index-url https://test.pypi.org/simple/ idmefv2
```

## Testing

Python unit tests using [`pytest`](https://docs.pytest.org/en/stable/) are provided:

``` sh
$ pytest
===================================================== test session starts =====================================================
platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0
rootdir: /SOME/WHERE/python-idmefv2
configfile: pyproject.toml
collected 4 items

idmefv2/test_message.py ....                                                                                            [100%]

====================================================== 4 passed in 0.12s ======================================================
```

## Examples

### Message modelization

A new message can be created by instantiating the `idmefv2.Message` class. This object can then be used like a regular Python dictionary:

``` python
# Import the Message class
from idmefv2 import Message

# Import other modules if necessary
import uuid
from datetime import datetime

# Keep track of the current date/time for later reference.
now = datetime.now().isoformat('T')

# Create the message and set its various properties.
msg = Message()
msg['Version'] = '0.1'
msg['ID'] = str(uuid.uuid4())
msg['CreateTime'] = now
msg['DetectTime'] = now
msg['CategoryRef'] = 'ENISA'
msg['Category'] = []
msg['Description'] = 'Someone tried to login as root from 12.34.56.78 '\
                     'port 1806 using the password method'
msg['Severity'] = 'medium'
msg['Ref'] = []
msg['Agent'] = {
    'Name': 'prelude-lml',
    'ID': str(uuid.uuid4()),
    'Category': ['LOG'],
    'IP4': '127.0.0.1',
    'IP6': '::1',
}
msg['Source'] = []
msg['Target'] = []

# Do something with the message (e.g. send it to a SIEM)
```

### Message validation

You can validate an IDMEFv2 message using its `validate()` method. A [validation error](https://python-jsonschema.readthedocs.io/en/stable/errors/) is raised if the message is invalid.

E.g.

``` python
try:
    msg.validate()
except jsonschema.exceptions.ValidationError as e:
    print("Validation failure: %s" % (e, ))
else:
    print("The message is valid")
```

### Message serialization/unserialization

Before the message can be sent to a remote system, it must be serialized.

To serialize a message, use the `serialize()` method, e.g.

``` python
result = msg.serialize('application/json')
```

The argument given to the `serialize()` method specifies the expected MIME content type for the resulting payload.

For the time being, only the `application/json` content type is supported, which results in a JSON-encoded message.

Likewise, when a message is received from a foreign system, it must be unserialized before it can be used. This is achieved using the `unserialize()` class method.

Please note that the received data must be encapsulated using an instance of the `SerializedMessage` class first so that the proper class can be used during the unserialization process based on the payload\'s content type.

E.g.

``` python
from idmefv2 import Message, SerializedMessage

# Instantiate a SerializedMessage based on the received data.
# The first argument specifies the MIME content type for the data.
payload = SerializedMessage('application/json', data)

# Unserialize the message for later use
msg = Message.unserialize(payload)

# Do something with the message (e.g. store it in a database)
```

## Contributions

All contributions must be licensed under the BSD 2-clause license. See the LICENSE file inside this repository for more information.

To improve coordination between the various contributors, we kindly ask that new contributors subscribe to the [IDMEFv2 mailing list](https://www.freelists.org/list/idmefv2) as a way to introduce themselves.
