import pika
import threading
import socket
import json
from models.votacao import Votacao
from models.usuario import Usuario

class Servidor:
    def __init__(self, host='localhost', port=5563, rabbitmq_host='189.8.205.54', rabbitmq_port=5672):
        self.host = host
        self.port = port
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.votacao = Votacao()
        self.resultados = {}

    def iniciar_servidor(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)

        print("Servidor iniciado e aguardando conexões...")

        threading.Thread(target=self.consumir_votos, daemon=True).start()
        threading.Thread(target=self.coletar_resultados_de_outros, daemon=True).start()

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
                resultados = self.get_resultados_agregados()
                resultado_str = "\n".join([f"Candidato {nome}: {votos} votos" for nome, votos in resultados.items()])
                conn.send(resultado_str.encode())

            elif mensagem == "sair":
                conn.send("Saindo da votação.".encode())
                break

        conn.close()

    def consumir_votos(self):
        try:
            credentials = pika.PlainCredentials('admin', 'admin')
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=credentials)
            )
            channel = connection.channel()
            channel.queue_declare(queue='votos')

            def callback(ch, method, properties, body):
                voto = json.loads(body.decode())
                cpf = voto['cpf']
                voto = voto['voto']
                self.votacao.registrar_voto(cpf, voto)
                print(f"Voto recebido: CPF={cpf}, Voto={voto}")

            channel.basic_consume(queue='votos', on_message_callback=callback, auto_ack=True)

            print('Aguardando votos. Pressione Ctrl+C para sair.')
            channel.start_consuming()

        except Exception as e:
            print(f"Erro ao conectar ao RabbitMQ: {e}")

    def coletar_resultados_de_outros(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', 0))  # Bind a uma porta disponível
            s.listen(5)
            while True:
                conn, addr = s.accept()
                with conn:
                    dados = conn.recv(1024).decode()
                    if dados:
                        resultados = json.loads(dados)
                        # Atualize seus resultados locais com os resultados recebidos
                        for cpf, votos in resultados.items():
                            if cpf in self.votacao.usuarios:
                                self.votacao.usuarios[cpf].votos += votos
                            else:
                                self.votacao.usuarios[cpf] = Usuario(cpf, votos)

    def get_resultados_agregados(self):
        resultados_locais = self.votacao.resultados()
        return resultados_locais
