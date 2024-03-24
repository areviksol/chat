import socket
import sys
import threading
from threading import Thread
import signal
import select

clients = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_all(clients, sender, message):
    for client in clients:
        if client != sender:
            client.send(message.encode())

class ClientHandler(Thread):
    def __init__(self, client_socket, addr, clients, name):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr
        self.clients = clients
        self.client_name = name

    def run(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    print("Client {} disconnected".format(self.addr))
                    self.client_socket.close()
                    self.clients.remove(self.client_socket)
                    break

                print("Received message from {}: {}".format(self.addr, data))

                message = "{}: {}".format(self.client_name, data)
                send_all(self.clients, self.client_socket, message)
            except Exception as e:
                print("Error occurred:", e)
                self.client_socket.close()
                if self.client_socket in self.clients:
                    self.clients.remove(self.client_socket)
                break

def main():
    global s
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        return

    host = "0.0.0.0"
    port = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))
    s.listen(5)

    print("Server listening on {}:{}".format(host, port))
    while True:
        try:
            client_socket, addr = s.accept()
            print("Got connection from", addr)
            name = client_socket.recv(1024).decode()
            print("Client name:", name)

            clients.append(client_socket)

            message = "server: client {} just arrived\n".format(name)
            send_all(clients, client_socket, message)

            handler = ClientHandler(client_socket, addr, clients, name)
            handler.daemon = True
            handler.start()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Exiting loop.")
            s.close()
            break
    print("After finally....")

if __name__ == "__main__":
    main()
