from __future__ import annotations
from urllib.parse import urlparse, parse_qsl
from luxon.http.handler import Handler
import re

class Request:
    def __init__(self, req: Handler) -> None:
        self.__handler = req
        self.__version = req.request_version
        self.__method = req.command
        self.__address = req.client_address
        self.__url = urlparse(req.path)
        self.__path = self.__url.path
        self.__query = dict(parse_qsl(self.__url.query))
        self.__headers = {key: str(value) for key, value in req.headers.items()}
        self.__groups = None

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