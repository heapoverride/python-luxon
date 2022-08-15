from __future__ import annotations
from typing import Any
from urllib.parse import urlparse, parse_qsl, unquote
import re
import json
from luxon.http.handler import Handler
from luxon.http.headers import ContentTypeHeader

class Request:
    def __init__(self, req: Handler) -> None:
        self.__handler = req
        self.__version = req.request_version
        self.__method = req.command
        self.__address = req.client_address
        self.__url = urlparse(req.path)
        self.__path = unquote(self.__url.path)
        self.__query = dict(parse_qsl(self.__url.query))
        self.__headers = {key: str(value) for key, value in req.headers.items()}
        self.__groups = None

        self.__body = self.__read_body()

        if "Content-Type" in self.headers:
            header = ContentTypeHeader.parse(self.headers["Content-Type"])
            #print(header.type, header.fields)
            if header.type in ("application/x-www-form-urlencoded",):
                # query string
                self.__body = dict(parse_qsl(self.__body))
            elif header.type in ("application/json",):
                # json
                self.__body = json.loads(self.__body)

    def __read_body(self) -> bytes | None:
        if "Content-Length" not in self.headers:
            return None
        return self.__handler.rfile.read(int(self.headers["Content-Length"]))

    @property
    def version(self) -> str:
        """HTTP version"""
        return self.__version

    @property
    def method(self) -> str:
        """HTTP method"""
        return self.__method

    @property
    def path(self) -> str:
        """HTTP path"""
        return self.__path

    @property
    def query(self) -> dict[str, str]:
        """HTTP query string"""
        return self.__query

    @property
    def headers(self) -> dict[str, str]:
        """HTTP request headers"""
        return self.__headers

    @property
    def body(self) -> bytes | list[Any] | dict[str, Any] | None:
        """HTTP request body"""
        return self.__body

    @property
    def address(self) -> tuple[str, int]:
        """Remote address"""
        return self.__address

    @property
    def groups(self) -> tuple[re.Match]:
        """Path regular expression groups"""
        return self.__groups

    @groups.setter
    def groups(self, value: tuple[re.Match]):
        self.__groups = value