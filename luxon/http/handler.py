import socketserver
from http.server import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    """Custom request handler"""
    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer) -> None:
        super().__init__(request, client_address, server)

    def do_GET(self): self.server.app.handle_request(self)
    def do_HEAD(self): self.server.app.handle_request(self)
    def do_POST(self): self.server.app.handle_request(self)
    def do_PUT(self): self.server.app.handle_request(self)
    def do_PATCH(self): self.server.app.handle_request(self)
    def do_DELETE(self): self.server.app.handle_request(self)
    def do_CONNECT(self): self.server.app.handle_request(self)
    def do_OPTIONS(self): self.server.app.handle_request(self)
    def do_TRACE(self): self.server.app.handle_request(self)