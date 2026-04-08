import struct


def encode(data):
    dim1 = len(data)
    dim2 = len(data[0])
    dim3 = len(data[0][0])

    buffer = bytearray()
    buffer.extend(struct.pack(">i", dim1))
    buffer.extend(struct.pack(">i", dim2))
    buffer.extend(struct.pack(">i", dim3))

    for matrix in data:
        if len(matrix) != dim2:
            raise ValueError("All matrices must have the same second dimension")
        for row in matrix:
            if len(row) != dim3:
                raise ValueError("All rows must have the same third dimension")
            buffer.extend(row)

    return buffer.hex()


def decode(encoded_hex):
    raw = bytes.fromhex(encoded_hex)
    dim1, dim2, dim3 = struct.unpack(">iii", raw[:12])

    offset = 12
    data = []
    for _ in range(dim1):
        matrix = []
        for _ in range(dim2):
            next_offset = offset + dim3
            matrix.append(raw[offset:next_offset])
            offset = next_offset
        data.append(matrix)

    return data
