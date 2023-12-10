import socket
import threading

HOST = "127.0.0.1"
PORT = 14045

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

name = input("Input your name: ")

def handle_client(conn, addr):
    print(f"Connected to {addr}")

    def receive_messages():
        while True:
            data = conn.recv(4096)
            if not data:
                print("Client disconnected")
                break
            print("")
            print(data.decode('utf-8'))

    def send_messages():
        while True:
            msg = input("Type your message ('Exit' to end the chat): ")
            if msg == "Exit":
                print("Disconnecting")
                conn.sendall(msg.encode("utf-8"))
                break
            else:
                full_msg = name + ": " + msg
                conn.sendall(full_msg.encode("utf-8"))

    # Start threads for both receiving and sending
    receive_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)

    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    conn.close()

while True:
    conn, addr = server.accept()

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
