from __future__ import annotations
from typing import Any, Callable
from luxon.app import App

class Router:
    """Router used by Luxon application"""
    def __init__(self) -> None:
        """Create new Router for Luxon application"""
        self.__routes: list[Router.Route] = []

    class Route:
        def __init__(self, *, method: str = "GET", path: str = "/", handler: Callable[[App.Re]] = None) -> None:
            """Create new Route"""
            self.method: str = method.upper()
            self.path: str = path
            self.handler: Callable = handler