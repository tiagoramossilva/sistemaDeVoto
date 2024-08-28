import socket

class Cliente:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port

    def iniciar_cliente(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

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
