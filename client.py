import socket
import sys
from threading import Thread

server_disconnected = False

def receive_messages(client_socket):
    global server_disconnected
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("Server disconnected")
                server_disconnected = True
                break
            print(data)
        except Exception as e:
            print("Error occurred:", e)
            break

def send_messages(client_socket):
    while True:
        try:
            if server_disconnected:
                break
            if not client_socket.fileno() == -1:
                message = input("")
                client_socket.send(message.encode())
            else:
                break
        except OSError as e:
            print("Error occurred:", e)
            break

def thread_cleanup(client_socket):
    client_socket.close()
    sys.exit()


def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_ip> <port>")
        return

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        name = input("Enter your name: ") 
        client_socket.connect((server_ip, port))
        print("Connected to server at {}:{}".format(server_ip, port))
        client_socket.send(name.encode())

        receive_thread = Thread(target=receive_messages, args=(client_socket,))
        try:
            receive_thread.daemon =True
            receive_thread.start()
        except:
            print("Error occurred during thread start:", e)
            thread_cleanup(client_socket)
            raise e
        send_thread = Thread(target=send_messages, args=(client_socket,))
        try:
            send_thread.daemon =True
            send_thread.start()
        except:
            print("Error occurred during thread start:", e)
            thread_cleanup(client_socket)
            raise e
        receive_thread.join()
        send_thread.join()
    except ConnectionRefusedError:
        print("Server is not running.") 
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Exiting client.")
    except SystemExit:
        print("SystemExit detected. Exiting client.")

if __name__ == "__main__":
    main()
