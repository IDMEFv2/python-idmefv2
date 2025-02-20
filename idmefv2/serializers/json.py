# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
'''
Serializer to JSON.

Classes:
    JSONSerializer
'''
import json

from ..exceptions import SerializationError
from ..message import Message
from ..serializer import Serializer

class JSONSerializer(Serializer):
    '''
    A class serializing/deserializing Message to/from JSON
    '''
    def serialize(self, message: Message) -> bytes:
        try:
            payload = json.dumps(message).encode('utf-8')
        except Exception as e:
            raise SerializationError() from e
        return payload

    def unserialize(self, payload: bytes) -> dict:
        try:
            message = json.loads(payload)
        except Exception as e:
            raise SerializationError() from e
        return message
