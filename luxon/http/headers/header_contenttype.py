from __future__ import annotations
from luxon.http.headers.header import Header

class ContentTypeHeader(Header):
    def __init__(self, type: str, fields: dict[str, str]) -> None:
        self.__type = type
        self.__fields = fields

    @property
    def type(self) -> str:
        return self.__type

    @property
    def fields(self) -> dict[str, str]:
        return self.__fields

    @staticmethod
    def parse(text: str) -> ContentTypeHeader:
        parts = [s.strip() for s in text.split(";")]

        content_type = parts[0]
        fields = {}

        for part in parts[1:]:
            name, value = part.split("=", maxsplit=1)
            fields[name] = value

        return ContentTypeHeader(content_type, fields)