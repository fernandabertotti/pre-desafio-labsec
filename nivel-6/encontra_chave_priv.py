import Byte2DEncoder, Byte3DEncoder
import hashlib

# Transformar digest em binário (está em hexadecimal)
# Verificar os bits do digest (0 ou 1) para rastrear a origem da chave privada
# Calcular o hash(revealed[i]) e comparar com public_key[i][0 ou 1]

# public_key : byte[256][2][32]
# digest : byte[32]
# revealed : byte[256][32]


with open("public_key.txt", "r") as f:
    public_key = Byte3DEncoder.decode(f.read().strip())

nums = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

digests = [] # Lista com todos os 10 digests em binário (256 bits cada)
revealeds = [] # Lista com todos os 10 revealeds em formato de array (256x32 cada)
for num in nums:
    with open(f"signature_{num}_digest.txt", "r") as f:
        digest_hex = f.read().strip()
        digest_bin = bin(int(digest_hex, 16))[2:].zfill(256)
        digests.append(digest_bin)
    with open(f"signature_{num}_revealed.txt", "r") as f:
        revealed_hex = f.read().strip()
        revealed_array = Byte2DEncoder.decode(revealed_hex) # revealed_array[256][32]
        revealeds.append(revealed_array)
        # Aqui você pode comparar o hash de revealed_bin com public_key[i][0 ou 1] para verificar a origem da chave privada

priv = [[None, None] for _ in range(256)]  # Inicializa a matriz da chave privada com None
for pos in range(10):
    for i in range(256):
        bit = int(digests[pos][i])
        h = hashlib.sha256(revealeds[pos][i]).digest()
        if h == public_key[i][bit]:
            priv[i][bit] = revealeds[pos][i]


# Verificar quantas posições ficaram completas
completas = sum(1 for i in range(256) if priv[i][0] is not None and priv[i][1] is not None)
print(f"Posições completas: {completas}/256")  

for pos in range(10):
    print(f"Digest {pos+1}, bit 75: {digests[pos][75]}")

for pos in range(10):
    h = hashlib.sha256(revealeds[pos][75]).digest()
    match_0 = (h == public_key[75][0])
    match_1 = (h == public_key[75][1])
    print(f"Sig {pos+1}: bit={digests[pos][75]}, match[0]={match_0}, match[1]={match_1}")

# No caso de bloco faltante, usar o valor da chave pública
for i in range(256):
    if priv[i][0] is None:
        print(f"Posição {i}: falta bloco 0")
        priv[i][0] = public_key[i][0]
    if priv[i][1] is None:
        print(f"Posição {i}: falta bloco 1")
        priv[i][1] = public_key[i][1]

# 1. Qual é o valor de pub[75][0]?
print(f"pub[75][0] = {public_key[75][0].hex()}")
print(f"pub[75][1] = {public_key[75][1].hex()}")
print(f"priv[75][1] = {priv[75][1].hex()}")

# 2. Verificar: hash(priv[75][1]) == pub[75][1]?
h = hashlib.sha256(priv[75][1]).digest()
print(f"hash(priv[75][1]) == pub[75][1]: {h == public_key[75][1]}")

# 3. Tentar: talvez priv[75][0] seja derivável de priv[75][1] de alguma forma?
# XOR com pub?
xor_attempt = bytes(a ^ b for a, b in zip(priv[75][1], public_key[75][0]))
print(f"XOR attempt hash match: {hashlib.sha256(xor_attempt).digest() == public_key[75][0]}")


resultado = Byte3DEncoder.encode(priv)



# 4. Verificar se o resultado hex está em minúsculas e sem problemas de formatação
print(f"Tamanho do resultado: {len(resultado)}")
print(f"Primeiros 50 chars: {resultado[:50]}")
print(f"Últimos 50 chars: {resultado[-50:]}")

# 1. Verificar se TODAS as 510 posições encontradas estão corretas
erros = 0
for i in range(256):
    for j in range(2):
        if priv[i][j] is not None:
            h = hashlib.sha256(priv[i][j]).digest()
            if h != public_key[i][j]:
                print(f"ERRO: posição {i}, bloco {j} não bate!")
                erros += 1
print(f"Total de erros: {erros}")

# 2. Verificar se alguma posição tem blocos iguais vindos de assinaturas diferentes
conflitos = 0
for i in range(256):
    for j in range(2):
        valores = set()
        for pos in range(10):
            bit = int(digests[pos][i])
            if bit == j:
                valores.add(revealeds[pos][i].hex())
        if len(valores) > 1:
            print(f"CONFLITO: posição {i}, bloco {j} tem {len(valores)} valores diferentes!")
            conflitos += 1
print(f"Total de conflitos: {conflitos}")

# 3. Tentar submeter SEM o header do encoder (raw hex)
raw = ""
for i in range(256):
    for j in range(2):
        if priv[i][j] is not None:
            raw += priv[i][j].hex()
        else:
            raw += public_key[i][j].hex()  # placeholder
print(f"Tamanho raw: {len(raw)}")
with open("private_key_raw.txt", "w") as f:
    f.write(raw)


#with open("private_key.txt", "w") as f:
#    f.write(resultado)
