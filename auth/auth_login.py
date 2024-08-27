# auth_login.py
import requests

def login_user(email, password):
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=YOUR_API_KEY'
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('Login successful')
        print(response.json())
    else:
        print('Error logging in')
        print(response.json())
