# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
'''
IDMEFv2 message validation, serialization and deserialization.

Classes:
    SerializedMessage
    Message
'''
import json
import re
import importlib.resources
import jsonschema

from .serializer import Serializer

class SerializedMessage:
    '''
    Container for a serialized IDMEFv2 message
    '''
    def __init__(self, content_type: str, payload: bytes) -> None:
        """
        Creates a new container for a serialized IDMEFv2 message.

        Parameters:
            content_type (str):
            The MIME type associated with the serialized payload.

            To promote interoperability, this SHOULD be a content type
            registered in IANA. A private MIME content type MAY be used
            when it is known that the next processing entity has support
            for that type.

            Whenever a private MIME content type is used, it MUST
            follow the naming conventions set forth by IANA.

            payload(bytes):
            The IDMEFv2 message, as a serialized payload.
        """
        self.content_type = content_type
        self.payload = payload

    def get_content_type(self) -> str:
        """
        Returns the content type associated with the serialized payload.
        """
        return self.content_type

    def __bytes__(self) -> bytes:
        """
        The serialized payload.
        """
        return self.payload


class Message(dict):
    '''
    A class to represent a IDMEFv2 message
    '''
    _SCHEMA_BASE_PACKAGE = 'idmefv2.schemas.drafts.IDMEFv2'
    _SCHEMA_RESOURCE = 'IDMEFv2.schema'

    def __init__(self):
        # The messages are empty right after initialization.
        pass

    def __get_version(self):
        version_in_message = self.get('Version')
        if version_in_message is None or not isinstance(version_in_message, str):
            return None
        pat = r'\d\.D\.V([\d]+)'
        m = re.match(pat, version_in_message)
        if m is None:
            return None
        version = m.group(1)
        return version

    def __get_schema_resource(self):
        version = self.__get_version()
        if version is not None:
            version_package = self._SCHEMA_BASE_PACKAGE + '.' + version
            if importlib.resources.files(version_package).joinpath(self._SCHEMA_RESOURCE).is_file():
                return importlib.resources.files(version_package).joinpath(self._SCHEMA_RESOURCE)
        latest_package = self._SCHEMA_BASE_PACKAGE + '.latest'
        return importlib.resources.files(latest_package).joinpath(self._SCHEMA_RESOURCE)

    def validate(self) -> None:
        '''
        Validate against the JSON schema corresponding
        to the IDMEFv2 version contained in the message.

        Raises a ValidationException if message is not valid w.r.t. schema.
        '''
        with self.__get_schema_resource().open('rb') as stream:
            try:
                jsonschema.validate(self, json.load(stream))
            finally:
                stream.close()

    def serialize(self, content_type: str) -> SerializedMessage:
        '''
        Serialize a message, selecting the proper Serializer according to the MIME type.

            Parameters:
                content_type (str): the MIME type of the wanted serialization data
        '''
        serializer = Serializer.get_serializer(content_type)
        self.validate()
        payload = serializer.serialize(self)
        return SerializedMessage(content_type, payload)

    @classmethod
    def unserialize(cls, payload: SerializedMessage) -> 'Message':
        '''
        Deserialize a payload, selecting the proper Serializer
        according to the MIME type of the payload.

            Parameters:
                payload (SerializedMessage): a SerializedMessage
                containing the bytes and the MIME type

            Returns:
                message(Message): the deserialized message
        '''
        serializer = Serializer.get_serializer(payload.get_content_type())
        fields = serializer.unserialize(bytes(payload))
        message = cls()
        message.update(fields)
        message.validate()
        return message
