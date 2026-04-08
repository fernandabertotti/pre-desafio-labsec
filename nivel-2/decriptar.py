# Importações da biblioteca 'cryptography'
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# openssl pkcs12 -in employee.p12 -nocerts -passin pass:'AVoiceFromBeyondTheGrave--867885998' -nodes -out chave_privada.pem

# --- PASSO 1: Carregar a chave privada ---
# Abrimos o arquivo .pem em modo binário ("rb" = read bytes)
# password=None porque extraímos a chave sem senha (-nodes)
with open("chave_privada.pem", "rb") as f:
    chave_privada = serialization.load_pem_private_key(f.read(), password=None)

# --- PASSO 2: Carregar o dado cifrado ---
# O .enc é um bloco bruto de bytes, então só lemos ele inteiro
with open("access_code.enc", "rb") as f:
    dado_cifrado = f.read()

# --- PASSO 3: Tentar decifrar com diferentes paddings ---
# Como não sabemos qual padding foi usado, testamos os principais.
# Cada tupla tem: (nome para exibição, objeto de padding)
tentativas = [
    ("PKCS1 v1.5", padding.PKCS1v15()),

    ("OAEP SHA1/MGF1-SHA1", padding.OAEP(
        mgf=padding.MGF1(hashes.SHA1()),       # sub-função MGF1 com SHA-1
        algorithm=hashes.SHA1(),                # hash principal SHA-1
        label=None)),

    ("OAEP SHA256/MGF1-SHA256", padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None)),

    ("OAEP SHA256/MGF1-SHA1", padding.OAEP(
        mgf=padding.MGF1(hashes.SHA1()),        # MGF1 com SHA-1
        algorithm=hashes.SHA256(),               # hash principal SHA-256
        label=None)),
]

# --- PASSO 4: Testar cada padding ---
for nome, pad in tentativas:
    try:
        # Tenta decifrar com este padding
        resultado = chave_privada.decrypt(dado_cifrado, pad)
        # Se chegou aqui sem erro, funcionou!
        # .decode('utf-8') converte bytes → texto legível
        print(f"{nome} → {resultado.decode('utf-8')}")
    except:
        # Se deu qualquer erro, esse padding não é o certo
        print(f"{nome} → falhou")