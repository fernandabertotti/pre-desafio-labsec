import hashlib

# 1. Ler o PDF como bytes e calcular SHAKE256 (512 bits = 64 bytes)
with open("instructions.pdf", "rb") as f:
    hash_pdf = hashlib.shake_256(f.read()).digest(64)

# 2. Calcular SHAKE256 da matrícula (como string UTF-8)
matricula = "24100601"
hash_mat = hashlib.shake_256(matricula.encode("utf-8")).digest(64)

# 3. XOR byte a byte
resultado = bytes(a ^ b for a, b in zip(hash_pdf, hash_mat))

# 4. Converter para hexadecimal (minúsculas, sem 0x)
with open("resultado.txt", "w") as f:
    f.write(resultado.hex())
