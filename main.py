import base64
import hashlib
import json
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
        client.close()
    except Exception as e:
        print(e)
        
def imprimir_bd():
    try:
        client = MongoClient("mongodb+srv://guizones:guigayreclamao@cluster-0.mo6jtw3.mongodb.net/")
        db = client["chat"]
        messages = db["messages"].find({"from": user})

        for i, message in enumerate(messages, 1):
            print(f"Mensagem {i}: {message['message']}")
            print()

        client.close()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


texto_chave_secreta = "Minha terra tem palmeira onde canta o sabiá, seno A . cos B + sen B . cos A"
key = gerar_chave_fernet(texto_chave_secreta.encode('utf-8'))
fernet = Fernet(key)
mensagem_em_claro = "Minha mensagem secreta..."
texto_cifrado = fernet.encrypt(mensagem_em_claro.encode('utf-8'))
texto_decifrado = fernet.decrypt(texto_cifrado).decode('utf-8')

print(f"string para gerar a chave: {texto_chave_secreta}")
print(f"mensagem_em_claro: {mensagem_em_claro}")
print(f"chave gerada em bytes: {key}")
print(f"chave gerada em impressão de string: {key.decode()}")
print(f"texto_cifrado: {texto_cifrado}")
print(f"texto_decifrado: {texto_decifrado}")

while True:
    user = input("Login: (Bob | Alice) - ")
    user = user.lower()
    print("Você está conectado como:", user)
    if user == "bob":
        to = "alice"
    else:
        to = "bob"
    case = input(f"O que você deseja? \n1 - Enviar mensagem secreta para {to}\n2 - Ler suas mensagens que estão no banco\n-> ")
    match case:
        case "1":
            message = input("Digite a mensagem que você deseja enviar - ")
            texto_cifrado = fernet.encrypt(mensagem_em_claro.encode('utf-8'))
            inserir_bd(user, to, False, texto_cifrado)
        case "2":
            print("Guizones e Eu faremos em goma")
            imprimir_bd()
            choice = int(input("Qual mensagem deseja ler? "))
            

