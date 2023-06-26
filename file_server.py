from socket import *
from io import StringIO
import socket
import threading
import logging

from file_protocol import FileProtocol
fp = FileProtocol()
logging.basicConfig(format='%(message)s', level=logging.WARNING)

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def recvall(self, num_bytes) -> str:
        buffer = StringIO()

        while True:
            data = self.connection.recv(num_bytes)
            if data:
                d = data.decode()
                buffer.write(d)

                if len(data) < num_bytes:
                    break
            else:
                break

        return buffer.getvalue()

    def run(self):
        d = self.recvall(4096)
        hasil = fp.proses_string(d)
        hasil = hasil+"\r\n\r\n"
        self.connection.sendall(hasil.encode())
        self.connection.close()


class Server(threading.Thread):
    def __init__(self, ipaddress='0.0.0.0', port=8889):
        self.ipinfo = (ipaddress, port)
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"ServerBind {self.ipinfo}")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"Client {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server(ipaddress='0.0.0.0', port=6666)
    svr.start()


if __name__ == "__main__":
    main()
