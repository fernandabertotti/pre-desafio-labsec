package br.ufsc.labsec.pbad.overdrive.utils;

import java.nio.ByteBuffer;
import java.util.HexFormat;

public class Byte3DEncoder {

    public static String encode(byte[][][] data) {
        int dim1 = data.length;
        int dim2 = data[0].length;
        int dim3 = data[0][0].length;

        int totalSize = 4 * 3 + (dim1 * dim2 * dim3); // 3 ints + data

        ByteBuffer buffer = ByteBuffer.allocate(totalSize);

        // store dimensions
        buffer.putInt(dim1);
        buffer.putInt(dim2);
        buffer.putInt(dim3);

        // flatten data
        for (byte[][] datum : data) {
            for (int j = 0; j < dim2; j++) {
                buffer.put(datum[j]);
            }
        }

        return HexFormat.of().formatHex(buffer.array());
    }

    public static byte[][][] decode(String encodedHex) {
        ByteBuffer buffer = ByteBuffer.wrap(HexFormat.of().parseHex(encodedHex));

        int dim1 = buffer.getInt();
        int dim2 = buffer.getInt();
        int dim3 = buffer.getInt();

        byte[][][] data = new byte[dim1][dim2][dim3];

        for (int i = 0; i < dim1; i++) {
            for (int j = 0; j < dim2; j++) {
                buffer.get(data[i][j]);
            }
        }

        return data;
    }
}
