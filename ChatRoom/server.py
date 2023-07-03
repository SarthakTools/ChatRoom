import socket
import threading

# Define server address and port
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5000
max_connection = 100

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(max_connection)

# List to store connected clients
clients = []

# Function to handle incoming messages from a client
def handle_client(client_socket, client_address):
    # Get client name
    client_name = client_socket.recv(1024).decode('utf-8')
    # Send welcome message to client
    client_socket.send(f'Welcome to the chat, {client_name}!'.encode('utf-8'))
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # If message is a private message, send it only to the specified recipient
                if message.startswith('/pm'):
                    # Extract recipient name and message from private message
                    recipient, message = message[4:].split(':', 1)
                    # Find client socket for recipient
                    recipient_socket = None
                    for client in clients:
                        if client != client_socket and client_name(client) == recipient:
                            recipient_socket = client
                            break
                    if recipient_socket is not None:
                        # Send private message to recipient
                        recipient_socket.send(f'(private) {client_name}: {message}'.encode('utf-8'))
                        # Send confirmation message to sender
                        client_socket.send(f'(private to {recipient}) {client_name}: {message}'.encode('utf-8'))
                    else:
                        # If recipient not found, send error message to sender
                        client_socket.send(f'Error: recipient {recipient} not found'.encode('utf-8'))
                # If message is a disconnect message, remove the client from the list of connected clients and stop handling messages
                elif message.startswith('/disconnect'):
                    clients.remove(client_socket)
                    client_socket.send(f'You have been disconnected.'.encode('utf-8'))
                    client_socket.close()
                    print(f'Client {client_name} disconnected.')
                    break
                # Otherwise, send message to all clients except the sender
                else:
                    for client in clients:
                        if client != client_socket:
                            client.send(f'{client_name}: {message}'.encode('utf-8'))
        except:
            # If an error occurs, remove the client from the list of connected clients and stop handling messages
            clients.remove(client_socket)
            print(f'Client {client_name} disconnected.')
            break

# Function to continuously accept incoming connections
def accept_connections():
    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        # Add client to list of connected clients
        clients.append(client_socket)
        print(f'Client {client_address} connected.')
        # Start handling messages from the client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start accepting incoming connections in a separate thread
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
