# client/cliente.py
import socket
from auth.firebase_config import autenticar_usuario

class Cliente:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port

    def iniciar_cliente(self):
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")

        if autenticar_usuario(email, senha):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))

            print("Conectado ao servidor.")
            client.send(email.encode())
            client.send(senha.encode())
            voto = input("Digite o número do candidato (1 para Candidato A, 2 para Candidato B): ")
            client.send(voto.encode())

            resposta = client.recv(1024).decode()
            print(resposta)

            client.close()
        else:
            print("Falha na autenticação.")
