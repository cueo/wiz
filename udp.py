import socket
from constants import PORT
from message import Request


class UDP:
    def __init__(self, ip: str):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (ip, PORT)

    def call(self, message: Request) -> bytes:
        self.sock.sendto(bytes(message), self.addr)
        data, _ = self.sock.recvfrom(1024)
        return data
