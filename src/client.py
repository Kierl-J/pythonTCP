import socket
import threading


HOST = '127.0.0.1' 
PORT = 6666        


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_socket.connect((HOST, PORT))


def receive_from_server():
    while True:
        try:
            data = client_socket.recv(1024)  # Receive data from the server
            if not data:
                print("Server closed the connection.")
                break
            print(f"Server says: {data.decode()}")
        except:
            print("Error receiving data.")
            break


receive_thread = threading.Thread(target=receive_from_server, daemon=True)
receive_thread.start()

while True:
    message = input("You (client), type a message to send to the server: ")
    if message.lower() == 'exit':
        print("Exiting...")
        client_socket.sendall(message.encode())
    client_socket.sendall(message.encode())


client_socket.close()
