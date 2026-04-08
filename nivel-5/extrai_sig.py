# hell -> 8
# Lust -> 8
# Gluttony -> 7
# Greed -> 6
# Anger -> 5
# Heresy -> 4 (A.X.I.O.M.)
# Violence -> 3 (Doc Faust)
# Fraud -> 2 (Null / Void)
# Treachery -> 1 (Silas 'Chrome' Vance)

with open("hell.pdf", "rb") as f:
    data = f.read()  # lê todo o PDF como bytes

import re

# Procura por assinaturas digitais no PDF
sig_matches = re.findall(rb'/Type\s*/Sig', data)
print(f"Found {len(sig_matches)} signatures")

# Para cada assinatura encontrada, extrai o conteúdo associado (PKCS#7)
matches = re.finditer(rb'/Contents\s*<([0-9a-fA-F\s\r\n]+)>', data, re.DOTALL)

# Remoção de espaços, quebras de linha e zeros à direita, e gravação dos arquivos DER
for i, m in enumerate(matches):
    hex_str = re.sub(r'[\s\r\n]', '', m.group(1).decode())
    hex_str = hex_str.rstrip('0')
    if len(hex_str) % 2:
        hex_str += '0'
    raw = bytes.fromhex(hex_str)
    with open(f"sig_{i}.der", "wb") as out:
        out.write(raw)