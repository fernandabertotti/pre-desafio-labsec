package br.ufsc.labsec.pbad.overdrive.utils;

import java.nio.ByteBuffer;
import java.util.HexFormat;

public class Byte2DEncoder {

    public static String encode(byte[][] data) {
        int dim1 = data.length;
        int dim2 = data[0].length;

        int totalSize = 4 * 2 + (dim1 * dim2); // 2 ints + data

        ByteBuffer buffer = ByteBuffer.allocate(totalSize);

        buffer.putInt(dim1);
        buffer.putInt(dim2);

        for (byte[] datum : data) {
            buffer.put(datum);
        }

        return HexFormat.of().formatHex(buffer.array());
    }

    public static byte[][] decode(String encodedHex) {
        ByteBuffer buffer = ByteBuffer.wrap(HexFormat.of().parseHex(encodedHex));

        int dim1 = buffer.getInt();
        int dim2 = buffer.getInt();

        byte[][] data = new byte[dim1][dim2];

        for (int i = 0; i < dim1; i++) {
            buffer.get(data[i]);
        }

        return data;
    }
}
