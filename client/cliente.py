import pika
import json

class Cliente:
    def __init__(self, rabbitmq_host='189.8.205.54', rabbitmq_port=5672):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.connection = None
        self.channel = None

    def configurar_conexao(self):
        """Configura a conexão e o canal com o RabbitMQ."""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='votos')
        self.channel.queue_declare(queue='resultados')

    def iniciar_cliente(self):
        """Inicia o cliente e começa a consumir mensagens da fila 'votos'."""
        if not self.channel:
            self.configurar_conexao()

        def callback(ch, method, properties, body):
            print(f"Mensagem recebida: {body.decode()}")

        self.channel.basic_consume(queue='votos', on_message_callback=callback, auto_ack=True)
        print("Aguardando mensagens. Pressione Ctrl+C para sair.")
        self.channel.start_consuming()

    def enviar_voto(self, cpf, voto):
        """Envia um voto para a fila 'votos'."""
        if not self.connection:
            self.configurar_conexao()

        voto_message = {'cpf': cpf, 'voto': voto}
        self.channel.basic_publish(exchange='', routing_key='votos', body=json.dumps(voto_message))
        print(f"Voto enviado: CPF={cpf}, Voto={voto}")

    def solicitar_resultados(self):
        """Solicita resultados da fila 'resultados'."""
        if not self.connection:
            self.configurar_conexao()

        self.channel.basic_publish(exchange='', routing_key='resultados', body='solicitar_resultados')
        print("Solicitação de resultados enviada")

    def fechar_conexao(self):
        """Fecha a conexão com o RabbitMQ."""
        if self.connection:
            self.connection.close()
            print("Conexão fechada.")

if __name__ == "__main__":
    cliente = Cliente()
    cliente.iniciar_cliente()
