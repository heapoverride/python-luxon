from __future__ import annotations
from typing import Any, Callable
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl
import socketserver
from luxon.html.tag import Tag

class App:
    """Luxon application"""
    def __init__(self) -> None:
        """Create new Luxon application"""
        super().__init__()
        self.__routes: list[App.Route] = []

    def route(self, method: str = "GET", path: str = "/"):
        """Add handler to new route

        Args:
            method (str, optional): HTTP method. Defaults to `"GET"`.
            path (str, optional): HTTP path. Defaults to `"/"`.
        """
        def decorator(func: Callable[[App.Request, App.Response], Any]) -> Callable[[App.Request, App.Response], Any]:
            self.__routes.append(App.Route(handler=func, method=method, path=path))
            return func
            
        return decorator

    def start(self, server_address: tuple[str, int]):
        """Start Luxon application

        Args:
            server_address (tuple[str, int]): _description_
        """
        with ThreadingHTTPServer(server_address, App.__RequestHandler) as httpd:
            #httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile="cert.pem", keyfile="key.pem")
            httpd.app = self
            httpd.serve_forever()

    def handle_request(self, _req: App.__RequestHandler):
        req = App.Request(_req)
        res = App.Response(_req)
        path = req.path.split("?")[0] # path without query string
        found = False

        for route in self.__routes:
            if req.method == route.method and path == route.path:
                found = True
                value = route.handler(req, res)
                if value != None: res.write(value)

        if not found:
            res.status = (404, "Route not Found")
            res.write()

        _req.wfile.flush()

    class Route:
        def __init__(self, *, method: str = "GET", path: str = "/", handler: Callable[[App.Re]] = None) -> None:
            """Create new Route"""
            self.method: str = method.upper()
            self.path: str = path
            self.handler: Callable = handler

    class __RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer) -> None:
            super().__init__(request, client_address, server)

        """Custom request handler"""
        def do_GET(self): self.server.app.handle_request(self)
        def do_HEAD(self): self.server.app.handle_request(self)
        def do_POST(self): self.server.app.handle_request(self)
        def do_PUT(self): self.server.app.handle_request(self)
        def do_PATCH(self): self.server.app.handle_request(self)
        def do_DELETE(self): self.server.app.handle_request(self)
        def do_CONNECT(self): self.server.app.handle_request(self)
        def do_OPTIONS(self): self.server.app.handle_request(self)
        def do_TRACE(self): self.server.app.handle_request(self)

    class Request:
        def __init__(self, req: App.__RequestHandler) -> None:
            self.__handler = req
            self.__version = req.request_version
            self.__method = req.command
            self.__path = req.path
            self.__address = req.client_address
            self.__headers = {key: str(value) for key, value in req.headers.items()}
            
            url = urlparse(self.path)
            self.__query = dict(parse_qsl(url.query))

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

    class Response:
        def __init__(self, req: App.__RequestHandler) -> None:
            self.__handler = req
            self.__headers_written = False
            self.__status = (200, "OK")
            self.__headers = {
                "Content-Type": "text/html"
            }

        @property
        def status(self) -> tuple[int, str]:
            """HTTP response status"""
            return self.__status

        @status.setter
        def status(self, value: tuple[int, str]):
            self.__status = value

        @property
        def headers(self) -> dict[str, str]:
            """HTTP response headers"""
            return self.__headers

        def __send_response(self, status: int = 200, message: str = None):
            """Send response status code

            Args:
                status (int): Status code. Defaults to 200 (OK).
                message (str, optional): Status message. Defaults to None.
            """
            self.__handler.send_response(status, message)

        def __send_headers(self, headers: dict[str, str]):
            """Send response headers

            Args:
                headers (dict[str, str]): HTTP response headers
            """
            for key, value in headers.items():
                self.__handler.send_header(key, value)

            self.__handler.end_headers()

        def write(self, data: str|bytes|Tag = None):
            """Write response body

            Args:
                data (str | bytes | Tag): _description_
                content_type (str, optional): _description_. Defaults to "text/html".
            """
            if not self.__headers_written:
                # Write response status and headers if they're not written yet
                self.__headers_written = True
                self.__send_response(*self.__status)
                self.__send_headers(self.__headers)

            if data != None:
                # Convert data to bytes
                if issubclass(type(data), Tag):
                    data = data.html().encode(encoding="utf-8")
                elif type(data) == str:
                    data = data.encode(encoding="utf-8")

                # Write response body
                self.__handler.wfile.write(data)