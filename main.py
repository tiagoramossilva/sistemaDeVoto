from server.servidor import Servidor
from client.cliente import Cliente

def main():
    opcao = input("Escolha 'servidor' para iniciar o servidor ou 'cliente' para iniciar o cliente: ")
    
    if opcao == 'servidor':
        servidor = Servidor()
        servidor.iniciar_servidor()
    elif opcao == 'cliente':
        cliente = Cliente()
        cliente.iniciar_cliente()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
