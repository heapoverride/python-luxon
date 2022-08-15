from __future__ import annotations
import re
from typing import Any, Callable
from luxon.http.request import Request
from luxon.http.response import Response

class Route:
    def __init__(self, *, method: str = "GET", path: str = "/", pattern: str = None, handler: Callable[[Request, Response], Any] = None) -> None:
        """Create new Route"""
        self.__method: str = method.upper()
        self.__path: str = path
        self.__pattern = re.compile(pattern) if pattern != None else None
        self.__handler: Callable = handler

    @property
    def method(self) -> str:
        """HTTP request method"""
        return self.__method

    @property
    def path(self) -> str:
        """HTTP request path"""
        return self.__path

    @property
    def pattern(self) -> re.Pattern:
        """Path regular expression (compiled)"""
        return self.__pattern

    @property
    def handler(self) -> Callable[[Request, Response], Any]:
        return self.__handler