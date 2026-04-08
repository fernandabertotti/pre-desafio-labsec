import Byte3DEncoder, hashlib

with open("final_answer.txt") as f:
    result = f.read().strip()

with open("public_key.txt") as f:
    pub = Byte3DEncoder.decode(f.read().strip())

priv = Byte3DEncoder.decode(result)

ok = 0
for i in range(256):
    for j in range(2):
        if hashlib.sha256(priv[i][j]).digest() == pub[i][j]:
            ok += 1
        else:
            print(f"Pos {i}, bloco {j}: não bate")

print(f"Blocos corretos: {ok}/512")