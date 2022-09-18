import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

size = 16

address = ("localhost", 10001)

sock.bind(address)
print("listen")
encoding = "utf-8"

sock.listen(1)

while True:
    print("Wait a connection")
    connection, address = sock.accept()
    print("New connection: ", address)

    for i in range(10):
        data = connection.recv(size)
        try:
            parts = int(data.decode())
        except:
            continue
        massage = ""
        for i in range(parts):
            data = connection.recv(size)
            massage = f'{massage}{data.decode(encoding)}'
        if data:
            print("Msg from client:",massage)
        else:
            print("Empty data")

        connection.sendall("OK".encode(encoding))

    connection.close()