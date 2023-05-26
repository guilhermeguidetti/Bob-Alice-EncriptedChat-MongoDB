"""
Neste exemplo utilizamos o Fernet com o uma lib encapsulada que já contem
todos os pacotes necessários para usar o modo CBC.
Não precisamos informar uma chave criptografada, neste caso a chave é gerada
(podemos exibí-la).
"""
import base64
import hashlib
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# lembre-se de instalar o módulo cryptography com o comando
# pip install cryptography
from cryptography.fernet import Fernet


# para gerar uma chave no fernet precisamos
# garantir que essa "string" depois de transformada em bytes
# gere uma chave em bytes que possa ser "codada" em base64 (apenas uma exigência do modo Fernet CBC)
def gerar_chave_fernet(chave: bytes) -> bytes:
    assert isinstance(chave, bytes)
    hlib = hashlib.md5()
    hlib.update(chave)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

#mongodb+srv://guizones:guigayreclamao@cluster-0.mo6jtw3.mongodb.net/?retryWrites=true&w=majority
def conexao_bd(uri, db):
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client[db]
    except Exception as e:
        print(e)

def inserir_bd(origin, to, wasRead, message):
    data = {
        "from": origin,
        "to": to,
        "wasRead": wasRead,
        "message": message
    }
    
    jayson = json.dumps(data)
    try:
        db = conexao_bd("mongodb+srv://guizones:guigayreclamao@cluster-0.mo6jtw3.mongodb.net/?retryWrites=true&w=majority", "chat")
        db["messages"].insert_one(json.loads(jayson))
    except Exception as e:
        print(e)

texto_chave_secreta = "Minha terra tem palmeira onde canta o sabiá, seno A . cos B + sen B . cos A"

# derivando a chave a partir do texto secreto.
key = gerar_chave_fernet(texto_chave_secreta.encode('utf-8'))
fernet = Fernet(key)
mensagem_em_claro = "Minha mensagem secreta..."
texto_cifrado = fernet.encrypt(mensagem_em_claro.encode('utf-8'))
texto_decifrado = fernet.decrypt(texto_cifrado).decode('utf-8')

# fazendo os prints para ver o resultado
print(f"string para gerar a chave: {texto_chave_secreta}")
print(f"mensagem_em_claro: {mensagem_em_claro}")
print(f"chave gerada em bytes: {key}")
print(f"chave gerada em impressão de string: {key.decode()}")
print(f"texto_cifrado: {texto_cifrado}")
print(f"texto_decifrado: {texto_decifrado}")


while True:
    user = input("Login: (Bob | Alice) - ")
    user = user.lower()
    print(user)
    print("Você está conectado como: ", user)
    if(user == "bob"):
        to = "alice"
    else:
        to = "bob"
    message = input("Digite a mensagem que você deseja enviar - ")
    inserir_bd(user, to, False, message)


