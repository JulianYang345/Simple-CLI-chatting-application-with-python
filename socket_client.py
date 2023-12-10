import socket
import threading

HOST = "127.0.0.1"
PORT = 14045

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

name = input("Input your name: ")
print("Connected to the server.")

def receive_messages():
    while True:
        data = client.recv(4096)
        if not data:
            print("Server disconnected")
            break
        print("")
        print(data.decode("utf-8"))

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    msg = input("Type your message ('Exit' to end the chat): ")

    # Handling send msg dari client
    if msg == "Exit":
        print("Terminating chat")
        client.sendall(msg.encode("utf-8"))
        break
    else:
        full_msg = name + ": " + msg
        client.sendall(full_msg.encode("utf-8"))

# Wait for the receive thread to finish
receive_thread.join()
client.close()
