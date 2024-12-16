# Copyright (C) 2021 CS GROUP - France. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import json
import re
import importlib.resources
import jsonschema

from .serializer import get_serializer

class SerializedMessage(object):
    def __init__(self, content_type: str, payload: bytes) -> None:
        """
        Creates a new container for a serialized IDMEFv2 message.

        @param content_type:
            The MIME type associated with the serialized payload.

            To promote interoperability, this SHOULD be a content type
            registered in IANA. A private MIME content type MAY be used
            when it is known that the next processing entity has support
            for that type.

            Whenever a private MIME content type is used, it MUST
            follow the naming conventions set forth by IANA.

        @param payload:
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
            if importlib.resources.is_resource(version_package, self._SCHEMA_RESOURCE):
                return importlib.resources.files(version_package).joinpath(self._SCHEMA_RESOURCE)
        latest_package = self._SCHEMA_BASE_PACKAGE + '.latest'
        return importlib.resources.files(latest_package).joinpath(self._SCHEMA_RESOURCE)

    def validate(self) -> None:
        with self.__get_schema_resource().open('rb') as stream:
            try:
                jsonschema.validate(self, json.load(stream))
            finally:
                stream.close()

    def serialize(self, content_type: str) -> SerializedMessage:
        serializer = get_serializer(content_type)
        self.validate()
        payload = serializer.serialize(self)
        return SerializedMessage(content_type, payload)

    @classmethod
    def unserialize(cls, payload: SerializedMessage) -> 'Message':
        serializer = get_serializer(payload.get_content_type())
        fields = serializer.unserialize(bytes(payload))
        message = cls()
        message.update(fields)
        message.validate()
        return message
