import  socket


def divide_msg(msg: str, size) -> int:
    massage_size = len(msg)
    part = massage_size // size
    if massage_size % size != 0:
        part += 1
    return part


def wtf(part):
    count = 0
    while part > 0:
        part //= 10
        count += 1
    return count

address = ("localhost", 10001)
size = 16

encoding = "utf-8"
massage = "fsdfspodjglsjgdkhgkdfbjkgbdkvjwesds"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(address)

part = divide_msg(massage, size)
sock.send(f"{part}{' ' * (size-wtf(part))}".encode(encoding))
for i in range(part):
    sock.send(f"{massage[i * size: (i + 1) * size ]}".encode(encoding))


data = sock.recv(size)
if data:
    data = data.decode(encoding)
    print("Successfully recieved from server")
else:
    print("smthg WRONG")