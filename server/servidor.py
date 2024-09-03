import pika
import threading

class Servidor:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='189.8.205.54',
                port=5672,
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='votos')
        self.channel.queue_declare(queue='resultados')

    def iniciar_servidor(self):
        print("Servidor iniciado e aguardando conexões...")
        # Cria conexões e canais separados para cada thread
        threading.Thread(target=self.iniciar_consumo_votos, daemon=True).start()
        threading.Thread(target=self.iniciar_consumo_resultados, daemon=True).start()
        # Mantém o programa em execução
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Servidor encerrado.")
            self.connection.close()

    def iniciar_consumo_votos(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='189.8.205.54',
                port=5672,
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='votos')

        def callback(ch, method, properties, body):
            voto = body.decode()
            print(f"Voto recebido: {voto}")
            # Processa o voto

        channel.basic_consume(queue='votos', on_message_callback=callback, auto_ack=True)
        print("Aguardando votos. Pressione Ctrl+C para sair.")
        channel.start_consuming()

    def iniciar_consumo_resultados(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='189.8.205.54',
                port=5672,
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='resultados')

        def callback(ch, method, properties, body):
            resultado = body.decode()
            print(f"Resultado recebido: {resultado}")
            # Processa o resultado

        channel.basic_consume(queue='resultados', on_message_callback=callback, auto_ack=True)
        print("Aguardando resultados de outros servidores. Pressione Ctrl+C para sair.")
        channel.start_consuming()

if __name__ == "__main__":
    servidor = Servidor()
    servidor.iniciar_servidor()
