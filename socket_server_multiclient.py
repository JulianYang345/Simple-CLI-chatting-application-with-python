import socket
import select

HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

name = input("Input your name: ")

# List to keep track of connected clients
clients = []

while True:
    readable, _, _ = select.select([server] + clients, [], [], 0.1)

    for sock in readable:
        if sock == server:
            conn, addr = server.accept()
            clients.append(conn)
            print(f"Client {addr} connected.")
        else:
            data = sock.recv(4096)
            if not data:
                print(f"Client {sock.getpeername()} disconnected.")
                clients.remove(sock)
            else:
                print(data.decode("utf8"))

    msg = input("Type your message: ")
    print("Type (exit) to disconnect")
    print("")

    if msg == "exit":
        break

    recipient = input("Enter the name of the recipient: ")
    private_msg = name + " (private to " + recipient + "): " + msg
    for client_sock in clients:
        if client_sock != server and client_sock.getpeername() == (HOST, PORT) and client_sock != server:
            client_sock.send(private_msg.encode('utf8'))

for client_sock in clients:
    client_sock.close()

server.close()
