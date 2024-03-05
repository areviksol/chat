import socket
import sys
from threading import Thread

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            print("Server disconnected")
            break
        print("Received message:", data)

def send_messages(client_socket):
    while True:
        message = input("Enter your message: ")
        client_socket.send(message.encode())

def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_ip> <port>")
        return

    server_ip = sys.argv[1]
    port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        print("Connected to server at {}:{}".format(server_ip, port))

        receive_thread = Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        send_thread = Thread(target=send_messages, args=(client_socket,))
        send_thread.start()

        receive_thread.join()
        send_thread.join()
        
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
