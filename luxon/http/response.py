from __future__ import annotations
import socket
import mimetypes

class Response:
    def __init__(self, socket: socket.socket) -> None:
        self.__sock = socket
        self.__status = Response.Status()
        self.__headers: dict[str, str|int] = {
            "Server":       "Luxon",
            "Connection":   "keep-alive",
            "Content-Type": "text/html; charset=utf-8"
        }
        self.__headers_sent = False

    @property
    def socket(self) -> socket.socket:
        """Socket associated with this response"""
        return self.__sock

    @property
    def status(self) -> Response.Status:
        """Response status"""
        return self.__status

    @property
    def headers(self) -> dict[str, str|int]:
        """Response headers"""
        return self.__headers

    def __send_line(self, header: str):
        self.socket.send(f"{header}\r\n".encode(encoding="utf-8"))

    def __send_headers(self):
        if not self.__headers_sent:
            self.__send_line(f"HTTP/1.1 {self.__status.code} {self.__status.message}")

            for header, value in self.__headers.items():
                self.__send_line(f"{header}: {value}")
                
            self.__send_line("")
            self.__headers_sent = True

    def send_headers(self):
        """Send response headers
        """
        if self.__headers_sent:
            raise Exception("Response headers can only be sent once per request.")
        self.__send_headers()

    def write(self, data: bytes):
        """Write response body

        Args:
            data (str | bytes | Tag | None): Response body data or None if empty response
        """
        if not self.__headers_sent:
            # Send response status and headers 
            # if they're not sent yet
            self.send_headers()

        # Write response body
        self.socket.send(data)

    def write_all(self, data: bytes):
        self.headers["Content-Length"] = len(data)
        self.write(data)

    def send_file(self, path: str):
        """Send file to client

        Args:
            path (str): Path to file
        """
        with open(path, "rb") as f:
            type, encoding = mimetypes.guess_type(path)
            self.headers["Content-Type"] = type if type != None else "application/octet-stream"
            f.seek(0, 2) # seek to end
            self.headers["Content-Length"] = f.tell()
            self.__send_headers()

            f.seek(0, 0) # seek to beginning

            while True:
                buffer = f.read(2048)

                if not buffer: 
                    break

                self.write(buffer)

    class Status:
        def __init__(self, code: int = 200, message: str = None) -> None:
            self.__code = code
            self.__message = message

            if message == None:
                _message = self.__get_message(code)
                if _message != None:
                    self.__message = _message

        @property
        def code(self) -> int:
            """Response status code"""
            return self.__code

        @code.setter
        def code(self, value: int):
            self.__code = value

            message = self.__get_message(value)
            if message != None:
                self.__message = message

        @property
        def message(self) -> str:
            """Response status message"""
            return self.__message

        @message.setter
        def message(self, value: str):
            self.__message = value

        def __get_message(self, code: int) -> str|None:
            for key, value in STATUS_CODES.items():
                if key == code:
                    return value
            return None

STATUS_CODES = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',
    103: 'Early Hints',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi-Status',
    208: 'Already Reported',
    226: 'IM Used',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Payload Too Large',
    414: 'URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Range Not Satisfiable',
    417: 'Expectation Failed',
    418: "I'm a Teapot",
    421: 'Misdirected Request',
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    425: 'Too Early',
    426: 'Upgrade Required',
    428: 'Precondition Required',
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    451: 'Unavailable For Legal Reasons',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    506: 'Variant Also Negotiates',
    507: 'Insufficient Storage',
    508: 'Loop Detected',
    509: 'Bandwidth Limit Exceeded',
    510: 'Not Extended',
    511: 'Network Authentication Required'
}