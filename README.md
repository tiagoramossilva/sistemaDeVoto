# Sistema de Votação Eletrônica Distribuída

## Descrição

Este é um sistema distribuído de votação eletrônica com autenticação via Firebase. O sistema permite que usuários votem em dois candidatos disponíveis, com autenticação por email e senha.

## Estrutura do Projeto

- `/auth` - Contém arquivos para autenticação e configuração do Firebase.
- `/models` - Contém classes para modelar usuários, candidatos e votação.
- `/server` - Contém o código para o servidor.
- `/client` - Contém o código para o cliente.
- `main.py` - Ponto de entrada do projeto.

## Como Rodar

1. Configure o Firebase e coloque o arquivo de credenciais em `auth/firebase_config.py`.
2. Execute o servidor:
    ```bash
    python main.py
    ```
3. Em outra janela do terminal, execute o cliente:
    ```bash
    python main.py
    ```

## Requisitos

- Python 3.x
- Firebase Admin SDK
