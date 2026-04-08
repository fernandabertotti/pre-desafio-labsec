import struct


def encode(data):
    dim1 = len(data)
    dim2 = len(data[0])

    buffer = bytearray()
    buffer.extend(struct.pack(">i", dim1))
    buffer.extend(struct.pack(">i", dim2))

    for row in data:
        if len(row) != dim2:
            raise ValueError("All rows must have the same length")
        buffer.extend(row)

    return buffer.hex()


def decode(encoded_hex):
    raw = bytes.fromhex(encoded_hex)
    dim1, dim2 = struct.unpack(">ii", raw[:8])

    offset = 8
    data = []
    for _ in range(dim1):
        next_offset = offset + dim2
        data.append(raw[offset:next_offset])
        offset = next_offset

    return data
