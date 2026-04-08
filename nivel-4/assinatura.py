from cryptography.hazmat.primitives import serialization

# Carrega o .pem e extrai n e d automaticamente
with open("chave_superior.pem", "rb") as f:
    chave = serialization.load_pem_private_key(f.read(), password=None)

numeros = chave.private_numbers()
n = numeros.public_numbers.n
d = numeros.d

# Lê o desafio
with open("number.txt") as f:
    desafio = int(f.read().strip(), base=16)

# RSA Textbook puro: desafio^d mod n
assinatura = pow(base=desafio, exp=d, mod=n)

# Resultado em hex, minúsculas, sem 0x
with open("assinatura.txt", "w") as f:
    f.write(hex(assinatura)[2:])