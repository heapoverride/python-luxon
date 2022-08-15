from __future__ import annotations
from urllib.parse import urlparse, parse_qsl, unquote
from luxon.http.handler import Handler
import re

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
    def body(self) -> bytes | None:
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