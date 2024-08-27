# auth_operations.py
import firebase_admin
from firebase_admin import auth

def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f'Successfully created user: {user.uid}')
    except Exception as e:
        print(f'Error creating user: {e}')
