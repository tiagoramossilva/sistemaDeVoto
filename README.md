Sistema de Votação Distribuído

Este é um sistema de votação distribuído implementado em Python, utilizando o RabbitMQ para comunicação entre clientes e servidores. O sistema permite que os usuários votem em um dos dois candidatos e vejam os resultados em tempo real.

Pré-requisitos

Certifique-se de ter as seguintes dependências instaladas em seu ambiente:
Python 3.x
RabbitMQ instalado e configurado

Bibliotecas Python

Você pode instalar a biblioteca necessária diretamente utilizando o pip. Execute o seguinte comando para instalar o pika:
pip install pika

Bibliotecas utilizadas:

pika (para comunicação com RabbitMQ)

Como Rodar o Projeto

1. Iniciar o Servidor
Antes de executar o cliente, inicie o servidor. O servidor será responsável por receber os votos e gerenciar o resultado da votação.


2. Iniciar o Cliente
Após iniciar o servidor, execute o cliente para votar ou visualizar os resultados.


Você pode realizar as seguintes operações:

1 para Votar
2 para Ver Resultados
3 para Sair
