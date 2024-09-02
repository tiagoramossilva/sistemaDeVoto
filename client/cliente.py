import pika
import json
import socket

class Cliente:
    def __init__(self, rabbitmq_host='189.8.205.54', rabbitmq_port=5672, servidor_host='localhost', servidor_port=5562):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.servidor_host = servidor_host
        self.servidor_port = servidor_port

    def enviar_voto(self, cpf, voto):
        credentials = pika.PlainCredentials('admin', 'admin')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='votos')

        mensagem = json.dumps({'cpf': cpf, 'voto': voto})
        channel.basic_publish(exchange='', routing_key='votos', body=mensagem)

        connection.close()

    def solicitar_resultados(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.servidor_host, self.servidor_port))
            s.sendall("resultados".encode())
            resultados = s.recv(4096).decode()
            print("Resultados recebidos:")
            print(resultados)

    def iniciar_cliente(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.servidor_host, self.servidor_port))

        cpf = input("Digite seu CPF sem pontuação (XXXXXXXXXXX): ")
        client.send(cpf.encode())  

        while True:
            comando = input("Digite 'voto' para votar, 'resultados' para ver resultados ou 'sair' para sair: ")
            if comando == 'voto':
                voto = input("Digite o número do candidato: 1 para Candidato A: Biscoito ou 2 para Candidato B: Bolacha): ")
                client.send(f"voto {voto}".encode())
                resposta = client.recv(1024).decode()
                print(resposta)
            
            elif comando == 'resultados':
                client.send("resultados".encode())
                resposta = client.recv(1024).decode()
                print(resposta)
            
            elif comando == 'sair':
                client.send("sair".encode())
                resposta = client.recv(1024).decode()
                print(resposta)
                break
            
            else:
                print("Comando inválido.")
        
        client.close()
