from server.servidor import Servidor
from client.cliente import Cliente

def main():
    escolha = input("Escolha 'servidor' para iniciar o servidor ou 'cliente' para iniciar o cliente: ")
    
    if escolha == 'servidor':
        servidor = Servidor()
        servidor.iniciar_servidor()
    elif escolha == 'cliente':
        cliente = Cliente()
        cliente.iniciar_cliente()  # Iniciar cliente já cuida do menu e das opções
    else:
        print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()
