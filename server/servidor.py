# server/servidor.py
import socket
import threading
from models.votacao import Votacao
from auth.firebase_config import autenticar_usuario

class Servidor:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.votacao = Votacao()

    def handle_client(self, conn, addr):
        print(f"Nova conexão: {addr}")
        while True:
            try:
                email = conn.recv(1024).decode()
                senha = conn.recv(1024).decode()
                if autenticar_usuario(email, senha):
                    voto = conn.recv(1024).decode()
                    if voto:
                        self.votacao.registrar_voto(int(voto))
                        conn.send("Voto registrado com sucesso!".encode())
                else:
                    conn.send("Autenticação falhou.".encode())
            except:
                break
        conn.close()

    def iniciar_servidor(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print("Servidor iniciado e aguardando conexões...")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
