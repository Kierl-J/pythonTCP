import socket
import threading


HOST = '127.0.0.1'
PORT = 6666

clients = []

# Function to handle communication with a client
def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"data received from {addr}: {data.decode()}")
            
            client_socket.sendall(b"data received!")
    except ConnectionResetError:
        print(f"Connection with {addr} was closed.")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection with {addr} closed.")

def handle_admin_input():
    while True:
        admin_message = input("Admin (type a message to send to clients): ")
        for client in clients:
            try:
                client.sendall(admin_message.encode())  # Send the admin's message to each client
                print(f"Sent to client: {admin_message}")
            except:
                print("Error sending message to client.")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

admin_thread = threading.Thread(target=handle_admin_input, daemon=True)
admin_thread.start()

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)  # Add the client to the list
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
