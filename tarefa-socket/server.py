import socket
import threading

from protocol import BUFFER_SIZE, MyProtocol

image_list = []

def server():
    server_address = ('0.0.0.0', 8080)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(server_address)

    server.listen(4)

    while True:
        client, address = server.accept()

        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()
        break

def handle_client(client: socket):
    data = client.recv(BUFFER_SIZE)

    message = data.decode()

    handle_protocol(client, message)

    client.close()

def handle_protocol(client: socket, protocol: MyProtocol):
    match protocol:
        case MyProtocol.DOWNLOAD:
            handle_download(client)
        case MyProtocol.UPLOAD:
            handle_upload(client)
        case MyProtocol.SEARCH:
            handle_search(client)

def handle_download():
    pass

def handle_upload():
    pass

def handle_search():
    pass

server()