import base64
import hashlib
import json
import cryptography
from pymongo import MongoClient
from datetime import datetime
from cryptography.fernet import Fernet


def gerar_chave_fernet(chave: bytes) -> bytes:
    assert isinstance(chave, bytes)
    hlib = hashlib.md5()
    hlib.update(chave)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def inserir_bd(origin, to, wasRead, message):
    data = {
        "from": origin,
        "to": to,
        "wasRead": wasRead,
        "message": message,
        "timestamp": datetime.now()
    }
    try:
        client = MongoClient("mongodb+srv://guizones:guigayreclamao@cluster-0.mo6jtw3.mongodb.net/")
        db = client["chat"]
        db["messages"].insert_one(data)
        print(origin + ", sua mensagem foi gravada no banco.")
        client.close()
    except Exception as e:
        print(e)
        
def imprimir_bd(user):
    try:
        client = MongoClient("mongodb+srv://guizones:guigayreclamao@cluster-0.mo6jtw3.mongodb.net/")
        db = client["chat"]
        messages = db["messages"].find({"from": user})
        print()
        for i, message in enumerate(messages, 1):
            print(f"Mensagem {i}: {message['message'].decode('utf-8')}")
            print()

        client.close()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        
def decifrar_msg(choice, user):
    client = MongoClient("mongodb+srv://guizones:guigayreclamao@cluster-0.mo6jtw3.mongodb.net/")
    db = client["chat"]
    message = db["messages"].find_one({"from": user}, skip=choice-1)

    if message:
        try:
            secretkey = str(input("Qual sua chave secreta? "))
            key = gerar_chave_fernet(secretkey.encode('utf-8'))
            fernet = Fernet(key)

            texto_cifrado = message["message"]
            texto_decifrado = fernet.decrypt(texto_cifrado).decode('utf-8')

            print(f"Mensagem selecionada: {texto_cifrado.decode('utf-8')}")
            print(f"Mensagem decifrada: {texto_decifrado}")
            try:
                db["messages"].update_one({"_id": message["_id"]}, {"$set": {"wasRead": True}})
            except Exception as e:
                print(f"Ocorreu um erro ao tentar alterar a mensagem para 'lida': {e}")
            print(f"Mensagem {choice} marcada como lida.")
                
        except cryptography.fernet.InvalidToken:
            print("Erro ao decifrar a mensagem. Chave incorreta.")
        except Exception as e:
            print(f"Ocorreu um erro durante a descriptografia: {e}")
    else:
        print("Mensagem não encontrada.")
    print()
    client.close()



while True:
    try:
        user = input("Login: (Bob | Alice) - ")
        user = user.lower()
        if user != "bob" and user != "alice":
            raise ValueError("Usuário inválido. Por favor, escolha entre Bob e Alice.")
        logado = True
        while logado:
            print("Você está conectado como:", user)
            if user == "bob":
                to = "alice"
            else:
                to = "bob"
            case = input(f"O que você deseja? \n1 - Enviar mensagem secreta para {to}\n2 - Ler suas mensagens que estão no banco\n3 - Trocar de usuário\n-> ")
            if case == "1":
                message = input("Digite a mensagem que você deseja enviar - ")
                secretkey = input("Digite um pequeno texto para cifrar a mensagem - ")
                key = gerar_chave_fernet(secretkey.encode('utf-8'))
                fernet = Fernet(key)
                texto_cifrado = fernet.encrypt(message.encode('utf-8'))
                inserir_bd(user, to, False, texto_cifrado)
            elif case == "2":
                imprimir_bd(user)
                try:
                    choice = int(input("Qual mensagem deseja ler? "))
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número inteiro.")
                    continue
                decifrar_msg(choice, user)
            elif case == "3":
                logado = False
    except ValueError as e:
        print(str(e))

