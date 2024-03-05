# Chat Application

This is a simple chat application that allows multiple clients to connect to a server and exchange messages with each other.

## Features

- Allows multiple clients to connect to a server.
- Clients can send messages to the server, and the server will broadcast these messages to all connected clients.
- Clients receive messages from the server in real-time.

## Usage

1. First, start the server by running `python server.py <port>`. Replace `<port>` with the desired port number for the server to listen on.

2. Once the server is running, clients can connect to it using the client script. Run `python client.py <server_ip> <port>` on each client machine to connect to the server. Replace `<server_ip>` with the IP address of the server and `<port>` with the port number.

3. Once connected, clients can start sending messages. Messages sent by any client will be broadcasted to all other connected clients.

4. To exit the chat, simply close the client program.

## Dependencies

This program requires Python 3.x and the `socket` library.

## Contributors

- [Your Name]

Feel free to contribute to this project by submitting pull requests or reporting issues.

