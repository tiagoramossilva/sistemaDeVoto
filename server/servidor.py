import pika
import threading
from models.votacao import Votacao

class Servidor:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='189.8.205.54',
                port=5672,
                virtual_host='thanos',
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='votos', exchange_type='direct', durable=True)
        self.channel.queue_declare(queue='votos', durable=True)
        self.channel.queue_declare(queue='resultados', durable=True)
        self.channel.queue_bind(exchange='votos', queue='votos')
        self.channel.queue_bind(exchange='votos', queue='resultados')

        self.votacao = Votacao()

    def callback(self, ch, method, properties, body):
        mensagem = body.decode()
        if mensagem == 'solicitar_resultados':
            resultados = self.votacao.exportar_resultados()
            self.channel.basic_publish(exchange='votos', routing_key='resultados', body=resultados)
        else:
            cpf, candidato_id = mensagem.split(':')
            resposta = self.votacao.registrar_voto(cpf, int(candidato_id))
            print(resposta)

    def iniciar_servidor(self):
        self.channel.basic_consume(queue='votos', on_message_callback=self.callback, auto_ack=True)
        print("Servidor pronto. Aguardando votos e solicitações de resultados...")

        def consume_messages():
            self.channel.start_consuming()

        thread = threading.Thread(target=consume_messages)
        thread.start()

def main():
    servidor = Servidor()
    servidor.iniciar_servidor()

if __name__ == "__main__":
    main()
