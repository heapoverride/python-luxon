from __future__ import annotations
from typing import Callable
from luxon.utils import Event
import socket
import threading
import ipaddress

BUFFER_SIZE = 2048

class HttpServer():
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self, server_address: tuple[str, int]):
        """Bind server to specific address and port"""
        self.__sock.bind(server_address)

    def start(self):
        """Start accepting incoming connectiodns"""
        self.__sock.listen()
        self.__start_accept()

    def __start_accept(self):
        while True:
            # accept incoming connection
            sock, address = self.__sock.accept()

            # start a thread to handle accepted connection
            thread = threading.Thread(target=self.__accept, args=(sock, address))
            thread.start()
            thread.join()

    def __accept(self, sock: socket.socket, address: tuple[str, int]):
        """Accept incoming connection"""
        #print(f"Accepted connection from {address}")

        while True:
            buffer = sock.recv(BUFFER_SIZE)
            if not bytes: break