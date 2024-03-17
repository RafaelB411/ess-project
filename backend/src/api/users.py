from fastapi import HTTPException
from fastapi.responses import JSONResponse
import src.db.firebase_config as firebase_config
import re
from src.api.payment_method import register_user

def create_user(name, username, email, cpf, password):
    try:
        firebase_config.auth.create_user_with_email_and_password(email, password)

        print("User created.")
        data = {
            "name": name,
            "username": username,
            "email": email,
            "cpf": cpf,
        }
        firebase_config.db.child("users").child(data["username"]).set(data)
        register_user(username)
        print("Dados do usuário cadastrados com sucesso!")
        return JSONResponse(status_code=201, content="Usuário criado!")
    except Exception:
        raise HTTPException(status_code=400, detail="Não foi possível criar o usuário.")

def login_user(email, password):
    try:
        firebase_config.auth.sign_in_with_email_and_password(email, password)
        return "Usuário logado com sucesso!"
    except Exception:
        raise HTTPException(status_code=401, detail="Email/Username ou senha inválidos.")

def check_existing_fields(username, email, cpf):
    users = firebase_config.db.child("users").get().val()
    #Percorre os dados para ver se username, email ou cpf já existem
    for _, info in users.items():
        existing_username = info['username']
        existing_email = info['email']
        existing_cpf = info['cpf']

        if existing_username == username:
            raise HTTPException(status_code=400, detail="Username já existe.")
        
        if existing_email == email:
            raise HTTPException(status_code=400, detail="Email já existe.")
        
        if existing_cpf == cpf:
            raise HTTPException(status_code=400, detail="CPF já existe.")
        

def check_register_fields(name, username, email, cpf, password):
    if name == "" or username == "" or email == "" or cpf == "" or password == "" or name == "undefined" or username == "undefined" or email == "undefined" or cpf == "undefined" or password == "undefined":
        raise HTTPException(status_code=400, detail="Todos os campos devem ser preenchidos.")
    
    #Checar se nome só possui letras e acentos
    name_regex = r"[^\W\d_]+"
    if not re.fullmatch(name_regex, name.replace(" ", "")):
        raise HTTPException(status_code=400, detail="Nome só deve conter letras.")

    #Checar se username só possui letras e números
    if not username.isalnum():
        raise HTTPException(status_code=400, detail="Username só deve conter caracteres alfanuméricos.")

    #Verifica se o email é válido
    if not is_email(email):
        raise HTTPException(status_code=400, detail="Esse email é inválido.")

    #Checar se CPF possui 11 dígitos e se são todos números
    if len(cpf) != 11 or not (cpf.isdecimal()):
        raise HTTPException(status_code=400, detail="CPF está no formato inválido.")

    #Checar se a senha tem tamanho maior ou igual a 8 caracteres
    if len(password) < 8: 
        raise HTTPException(status_code=400, detail="Senha deve conter pelo menos 8 caracteres.")
    

def is_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.fullmatch(email_regex, email):
        return False
    return True

def get_email_from_username(username):
    email = firebase_config.db.child("users").child(username).child("email").get().val()
    if email is None:
        raise HTTPException(status_code=401, detail="Username inválido.")
    return email

def get_username_from_email(email):
    if email == "":
        return ""
    users = firebase_config.db.child("users").get().val()
    #Percorre os dados para procurar o email
    for _, info in users.items():
        existing_username = info['username']
        existing_email = info['email']

        if existing_email == email:
            return existing_username