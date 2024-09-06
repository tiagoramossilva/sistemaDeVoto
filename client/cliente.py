import pika
from models.usuario import Usuario
import threading

class Cliente:
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
        self.channel.queue_declare(queue='resultados', durable=True)
        self.channel.queue_bind(exchange='votos', queue='resultados')

        self.usuario = None
        self.resultados_recebidos = False

    def callback(self, ch, method, properties, body):
        resultado = body.decode()
        print("\nResultados recebidos:")
        print(resultado)
        self.resultados_recebidos = True
        self.channel.stop_consuming()

    def iniciar_cliente(self):
        print("Cliente pronto. Aguardando comandos...")
        while True:
            escolha = input("Escolha uma opção: 1 para Votar, 2 para Ver Resultados, 3 para Sair: ")
            if escolha == '1':
                self.votar()
            elif escolha == '2':
                thread_resultados = threading.Thread(target=self.ver_resultados)
                thread_resultados.start()
            elif escolha == '3':
                print("Saindo...")
                self.connection.close()
                break
            else:
                print("Opção inválida.")

    def votar(self):
        if not self.usuario:
            cpf = input("Digite seu CPF para continuar: ")
            self.usuario = Usuario(cpf)

        if self.usuario.votou:
            print("Você já votou.")
            return

        candidato_id = input("Digite o número do seu candidato 1 - para Candidato A ou 2 - para Candidato B: ")
        mensagem = f"{self.usuario.cpf}:{candidato_id}"
        self.channel.basic_publish(exchange='votos', routing_key='votos', body=mensagem)
        self.usuario.votar()
        print("Voto enviado.")

    def ver_resultados(self):
        self.resultados_recebidos = False
        self.channel.basic_publish(exchange='votos', routing_key='votos', body='solicitar_resultados')
        print("Aguardando resultados...")

        self.channel.basic_consume(queue='resultados', on_message_callback=self.callback, auto_ack=True)

        while not self.resultados_recebidos:
            self.connection.process_data_events()


def main():
    cliente = Cliente()
    cliente.iniciar_cliente()

if __name__ == "__main__":
    main()
