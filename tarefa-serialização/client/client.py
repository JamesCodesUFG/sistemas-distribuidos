import socket

from valk import Flag, Valk

BUFFER_SIZE = 128

SERVER_ADDRESS = ('192.168.6.149', 27015)

def create_socket():
    server_address = (SERVER_ADDRESS)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(server_address)

    return client

def get() -> bytes:
    client = create_socket()

    client.send('GET'.encode())

    response = b''

    while True:
        data = client.recv(BUFFER_SIZE)

        if data != b'':
            response = response + data
        else:
            break 

    client.close()

    return response

def post(data: bytes):
    client = create_socket()

    client.send('POST'.encode())

    for inner in range(0, len(data), BUFFER_SIZE):
        client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

    client.close()

