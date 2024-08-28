import socket
import threading
from models.votacao import Votacao
from models.usuario import Usuario

class Servidor:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.votacao = Votacao()

    def iniciar_servidor(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)

        print("Servidor iniciado e aguardando conexões...")

        while True:
            conn, addr = server.accept()
            print(f"Conectado a {addr}")
            threading.Thread(target=self.tratar_cliente, args=(conn,)).start()

    def tratar_cliente(self, conn):
        cpf = conn.recv(1024).decode()
        if cpf not in self.votacao.usuarios:
            self.votacao.usuarios[cpf] = Usuario(cpf)

        while True:
            mensagem = conn.recv(1024).decode()
            if not mensagem:
                break

            if mensagem.startswith("voto"):
                _, voto = mensagem.split()
                resposta = self.votacao.registrar_voto(cpf, int(voto))
                conn.send(resposta.encode())

            elif mensagem == "resultados":
                resultados = self.votacao.resultados()
                resultado_str = "\n".join([f"{nome}: {votos} votos" for nome, votos in resultados.items()])
                conn.send(resultado_str.encode())

            elif mensagem == "sair":
                conn.send("Saindo da votação.".encode())
                break

        conn.close()
