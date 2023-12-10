import socket
import select

HOST = "127.0.0.1"
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
  
name = input("Input your name: ")

while True:
    readable, _, _ = select.select([client], [], [], 0.1)

    for sock in readable:
        data = sock.recv(4096)
        if not data:
            print("Server disconnected.")
            client.close()
            break
        else:
            print(data.decode("utf8"))

    msg = input("Type your message: ")
    print("Type (exit) to disconnect")
    print("")

    if msg == "exit":
        client.send(b"disconnecting")
        client.close()
        break

    name_msg = name + ": " + msg
    client.send(name_msg.encode('utf8'))
