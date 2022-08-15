from luxon.http.handler import Handler
from luxon.html.tag import Tag

class Response:
    def __init__(self, req: Handler) -> None:
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
            data (str | bytes | Tag | None): Response body data or None if empty response
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