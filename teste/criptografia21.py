from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json



def criptografar(texto, chave):
    chave = chave.encode('utf-8')
    cipher = AES.new(chave, AES.MODE_CBC)

    iv = cipher.iv
    dados = pad(texto.encode('utf-8'), AES.block_size)

    criptografado = cipher.encrypt(dados)

    return iv + criptografado

def descriptografar(dados, chave):
    chave = chave.encode('utf-8')

    iv = dados[:16]
    criptografado = dados[16:]

    cipher = AES.new(chave, AES.MODE_CBC, iv=iv)

    texto = unpad(cipher.decrypt(criptografado), AES.block_size)

    return texto.decode('utf-8')

