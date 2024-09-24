import socket

def servidor_broadcast():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print("Servidor broadcast pronto para enviar mensagens...")

    while True:
        mensagem = input("Digite a mensagem para enviar: ")
        servidor_socket.sendto(mensagem.encode(), ('<broadcast>', 12346))

servidor_broadcast()