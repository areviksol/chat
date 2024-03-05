import socket
import sys
from threading import Thread

def send_all(clients, sender, message):
    for client in clients:
        if client != sender:
            client.send(message.encode())

class ClientHandler(Thread):
    def __init__(self, client_socket, addr, clients):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr
        self.clients = clients

    def run(self):
        while True:
            data = self.client_socket.recv(1024).decode()
            if not data:
                print("Client {} disconnected".format(self.addr))
                self.client_socket.close()
                self.clients.remove(self.client_socket)
                break

            print("Received message from {}: {}".format(self.addr, data))

            message = "client {}: {}\n".format(self.clients.index(self.client_socket), data)
            send_all(self.clients, self.client_socket, message)

def main():

    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        return

    host = '0.0.0.0'
    port = int(sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    print("Server listening on {}:{}".format(host, port))

    clients = []

    while True:
        client_socket, addr = s.accept()
        print("Got connection from", addr)

        clients.append(client_socket)

        message = "server: client {} just arrived\n".format(len(clients))
        send_all(clients, client_socket, message)

        handler = ClientHandler(client_socket, addr, clients)
        handler.start()

if __name__ == "__main__":
    main()
