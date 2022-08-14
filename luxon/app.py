from __future__ import annotations
from typing import Any, Callable
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import socketserver
from luxon.html.tag import Tag

class App:
    """Luxon application"""
    def __init__(self) -> None:
        """Create new Luxon application"""
        super().__init__()
        self.__routes: list[App.Route] = []

    @property
    def routes(self) -> list[App.Route]:
        """Get list of routes

        Returns:
            list[Router.Route]: List of routes
        """
        return self.__routes

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

        for route in self.routes:
            if req.method == route.method and req.path == route.path:
                value = route.handler(req, res)
                if value != None: res.write(value)
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

        def send_response(self, status: int = 200, message: str = None):
            """Send response status code

            Args:
                status (int): Status code. Defaults to 200 (OK).
                message (str, optional): Status message. Defaults to None.
            """
            self.__handler.send_response(status, message)

        def send_headers(self, headers: dict[str, str]):
            """Send response headers

            Args:
                headers (dict[str, str]): HTTP response headers
            """
            for key, value in headers.items():
                self.__handler.send_header(key, value)

            self.__handler.end_headers()

        def set_status(self, status: int, message: str = None):
            """Set response status code

            Args:
                status (int): _description_
                message (str, optional): _description_. Defaults to None.
            """
            self.__status = (status, message)

        def set_header(self, header: str, value: str):
            """Set response header value

            Args:
                header (str): _description_
                value (str): _description_
            """
            self.__headers[header] = value

        def write(self, data: str|bytes|Tag):
            """Write response body

            Args:
                data (str | bytes | Tag): _description_
                content_type (str, optional): _description_. Defaults to "text/html".
            """
            if not self.__headers_written:
                # Write response status and headers if they're not written yet
                self.__headers_written = True
                self.send_response(*self.__status)
                self.send_headers(self.__headers)

            # Convert data to bytes
            if issubclass(type(data), Tag):
                data = data.html().encode(encoding="utf-8")
            elif type(data) == str:
                data = data.encode(encoding="utf-8")

            # Write response body
            self.__handler.wfile.write(data)