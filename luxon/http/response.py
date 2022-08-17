import socket

class Response:
    def __init__(self, socket: socket.socket) -> None:
        self.__sock = socket
        self.__status: tuple[int, str] = (200, "OK")
        self.__headers: dict[str, str] = {}
        self.__headers_sent = False

    @property
    def socket(self) -> socket.socket:
        """Socket associated with this response"""
        return self.__sock

    @property
    def status(self) -> tuple[int, str]:
        """Response status"""
        return self.__status

    @status.setter
    def status(self, value: tuple[int, str]):
        self.__status = value

    @property
    def headers(self) -> dict[str, str]:
        """Response headers"""
        return self.__headers