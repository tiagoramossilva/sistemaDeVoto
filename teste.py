import pika

def test_connection():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='189.8.205.54',
                port=5672,
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        print("Conexão bem-sucedida!")
        connection.close()
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    test_connection()
