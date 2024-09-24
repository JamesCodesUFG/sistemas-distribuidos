import socket

def cliente_broadcast():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    cliente_socket.bind(("0.0.0.0", 12346))
    print("Cliente aguardando mensagens de broadcast...")

    while True:
        mensagem, endereco = cliente_socket.recvfrom(1024)
        print(f"Mensagem recebida de {endereco}: {mensagem.decode()}")

cliente_broadcast()