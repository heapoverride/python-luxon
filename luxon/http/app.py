from __future__ import annotations
from typing import Any, Callable
from luxon.http.server import HttpServer
from luxon.http.request import Request
from luxon.http.response import Response
from luxon.http.route import Route

class App:
    """Luxon application"""
    def __init__(self, path: str = "/") -> None:
        """Create new Luxon application"""
        super().__init__()

        self.__path = path
        self.__routes: list[Route] = []

        self.__server = HttpServer()
        self.__server.on_request += self.__request_handler

    @property
    def path(self) -> str:
        """App path"""
        return self.__path

    def route(self, method: str = "GET", path: str = "/", pattern: str = None):
        """Add handler to new route

        Args:
            method (str, optional): HTTP method. Defaults to `"GET"`.
            path (str, optional): HTTP path. Defaults to `"/"`.
        """
        def decorator(func: Callable[[Request, Response], Any]) -> Callable[[Request, Response], Any]:
            self.__routes.append(Route(handler=func, method=method, path=path, pattern=pattern))
            return func
            
        return decorator

    def start(self, server_address: tuple[str, int]):
        """Start Luxon application

        Args:
            server_address (tuple[str, int]): _description_
        """
        self.__server.bind(server_address)
        self.__server.start()

    def __request_handler(self, request: Request, response: Response):
        pass

    """def __request_handler(self, request: Request, response: Response):
        path = request.path.split("?")[0] # path without query string
        found = False

        if path.startswith(self.path):
            # app path
            if self.path != "/":
                path = path[len(self.path):]
                if path == "": path = "/"

            for route in self.__routes:
                # check request method
                if request.method != route.method:
                    continue

                if route.pattern != None:
                    # check pattern
                    match = route.pattern.search(path)

                    if match != None:
                        request.groups = match.groups()
                        found = True
                        value = route.handler(request, response)
                        if value != None: response.write(value)

                # check path
                elif path == route.path:
                    found = True
                    value = route.handler(req, response)
                    if value != None: response.write(value)

        # route not found
        if not found:
            response.status = (404, "Route Not Found")
            response.write()

        # flush response buffer
        _req.wfile.flush()"""