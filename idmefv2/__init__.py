# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
'''
Handle validation, serialization and deserialization of IDMEFv2 messages.

About IDMEFv2, see https://idmefv2.ovh/ and https://github.com/IDMEFv2/

Classes:
    Message
    SerializedMessage
    Serializer

'''
from .message import (
    Message,
    SerializedMessage,
)

from .serializer import (
    Serializer,
)

from .exceptions import (
    SerializationError,
)
