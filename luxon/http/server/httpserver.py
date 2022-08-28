from __future__ import annotations
from typing import Callable
from luxon.utils import Event
from luxon.consts import *
import socket
import threading
import ipaddress
from luxon.http.request import Request
from luxon.http.response import Response

class HttpServer():
    def __init__(self):
        self.__on_request = Event()
        self.__alive = True
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    @property
    def on_request(self):
        """Request event handler"""
        return self.__on_request

    @on_request.setter
    def on_request(self, value):
        self.__on_request = value

    def bind(self, server_address: tuple[str, int]):
        """Bind Luxon HTTP server to specific address and port"""
        self.__sock.bind(server_address)

    def start(self):
        """Start Luxon HTTP server"""
        self.__sock.listen()
        self.__start_accept()

    def stop(self):
        """Stop Luxon HTTP server"""
        self.__alive = False
        self.__sock.close()

    def __start_accept(self):
        try:
            while self.__alive:
                # accept incoming connection
                sock, address = self.__sock.accept()

                # start a thread to handle accepted connection
                thread = threading.Thread(target=self.__accept, args=(sock, address))
                thread.start()
                
        except KeyboardInterrupt:
            self.stop()
        except:
            pass

    def __accept(self, sock: socket.socket, address: tuple[str, int]):
        """Accept incoming connection"""
        # Log connection
        print(f"{address} > New connection")

        try:
            while self.__alive:
                # read request headers
                request = Request(sock)
                response = Response(sock)

                # Log request
                print(f"{address} > {request.method} {request.path}")

                # Call request event handler
                self.on_request(request, response)

                # Close socket if 'Connection: close'
                if "Connection" in request.headers and request.headers["Connection"] == "close":
                    sock.close()

        except KeyboardInterrupt:
            self.stop()
        except:
            pass