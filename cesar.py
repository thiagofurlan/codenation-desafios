import requests
import io
import json
import hashlib

def decifrar(cifrado, casas):
    decifrado = ""
    for c in cifrado:
        if ord(c) > 96 and ord(c) < 123:
            dif = ord(c) - casas
            if dif < 97:
                decifrado += chr(122 - (96-dif))
                continue
            decifrado += chr(ord(c) - casas)
        else:
            decifrado += c
    return decifrado

def criar_arquivo(token):
    f = open('answer.json', 'w')
    r = requests.get(f'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={token}')
    f.write(str(r.text))
    f.close()

def ler_arquivo():
    f = open('answer.json', )
    dados = json.load(f)
    f.close()
    return dados

def atualizar_arquivo(dados, decifrado, resumo_criptografico):
    dados['decifrado'] = decifrado
    dados['resumo_criptografico'] = resumo_criptografico
    f = open('answer.json', 'w')
    f.write(json.dumps(dados))
    f.close()

def gerar_sha1(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

def send_codenation(token):
    files = {'answer': open('answer.json', 'rb')}
    r = requests.post(f'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={token}', files=files)
    return r.text

token = 'b682977caa30bf74ca615dc47b83bcd4c6519e7e'

criar_arquivo(token)
dados = ler_arquivo()
casas = dados['numero_casas']
cifrado = dados['cifrado']
decifrado = decifrar(cifrado, casas)
resumo_criptografico = gerar_sha1(decifrado)

atualizar_arquivo(dados, decifrado, resumo_criptografico)

print(send_codenation(token))