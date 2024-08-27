import firebase_admin 
from firebase_admin import credentials

cred = credentials.Certificate("sistema-de-votacao-distribuido-firebase-adminsdk-je0o8-b5c1f757e6.json")
firebase_admin.initialize_app(cred)

def autenticar_usuario():
    # Implementação da função
    pass
