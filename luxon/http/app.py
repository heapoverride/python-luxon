from __future__ import annotations
from typing import Any, Callable
from http.server import ThreadingHTTPServer
from luxon.http.handler import Handler
from luxon.http.route import Route
from luxon.http.request import Request
from luxon.http.response import Response

class App:
    """Luxon application"""
    def __init__(self, path: str = "/") -> None:
        """Create new Luxon application"""
        super().__init__()
        self.__path = path
        self.__routes: list[Route] = []

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
        with ThreadingHTTPServer(server_address, Handler) as httpd:
            #httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile="cert.pem", keyfile="key.pem")
            httpd.app = self
            httpd.serve_forever()

    def handle_request(self, _req: Handler):
        req = Request(_req)
        res = Response(_req)
        path = req.path.split("?")[0] # path without query string
        found = False

        if path.startswith(self.path):
            # app path
            path = path[len(self.path):]
            if path == "": path = "/"

            for route in self.__routes:
                # check request method
                if req.method != route.method:
                    continue

                if route.pattern != None:
                    # check pattern
                    match = route.pattern.search(path)

                    if match != None:
                        req.groups = match.groups()
                        found = True
                        value = route.handler(req, res)
                        if value != None: res.write(value)

                # check path
                elif path == route.path:
                    found = True
                    value = route.handler(req, res)
                    if value != None: res.write(value)

        # route not found
        if not found:
            res.status = (404, "Route Not Found")
            res.write()

        # flush response buffer
        _req.wfile.flush()