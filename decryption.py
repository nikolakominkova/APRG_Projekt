import constants as cn


def inv_sub_bytes(my_matrix):
    """This make inverse sub bytes."""
    split = []
    sub_b = []
    for i in my_matrix:
        for index in i:
            if index == "a":
                index = 10
            elif index == "b":
                index = 11
            elif index == "c":
                index = 12
            elif index == "d":
                index = 13
            elif index == "e":
                index = 14
            elif index == "f":
                index = 15
            split.append(index)
    for count in range(0, 16):
        i = int(split[count * 2])
        j = int(split[count * 2 + 1])
        sub_b.append(cn.INVERSE_S_BOX[i][j])
    sub_bytes = [sub_b[:4], sub_b[4:8], sub_b[8:12], sub_b[12:16]]
    return sub_bytes


def inv_shift_rows(s_b):
    """This make inverse shift rows."""
    shift_rows = [s_b[0], s_b[13], s_b[10], s_b[7], s_b[4], s_b[1], s_b[14], s_b[11], s_b[8], s_b[5], s_b[2], s_b[15],
                  s_b[12], s_b[9], s_b[6], s_b[3]]
    return shift_rows


def xor(a, b):
    """This make the XOR operation over two matrixes."""
    xor = ""
    for j in range(0, 8):
        if a[j] == b[j]:
            xor = xor + "0"
        else:
            xor = xor + "1"
    return xor


def mult9(a, b):
    """This multiply by 9."""
    return cn.mult9[a][b]


def mult11(a, b):
    """This multiply by 11."""
    return cn.mult11[a][b]


def mult13(a, b):
    """This multiply by 13."""
    return cn.mult13[a][b]


def mult14(a, b):
    """This multiply by 14."""
    return cn.mult14[a][b]


def inv_mix_columns(add_rk):
    """This make inverse mix columns."""
    mix = [["0e", "0b", "0d", "09"], ["09", "0e", "0b", "0d"], ["0d", "09", "0e", "0b"], ["0b", "0d", "09", "0e"]]
    mat = [add_rk[0:4], add_rk[4:8], add_rk[8:12], add_rk[12:16]]
    mix_c, my_list = [], []
    for k in mat:
        for j in range(4):
            matmul = []
            for m in range(4):
                split = []
                for i in k[m]:
                    if i == "a":
                        i = 10
                    elif i == "b":
                        i = 11
                    elif i == "c":
                        i = 12
                    elif i == "d":
                        i = 13
                    elif i == "e":
                        i = 14
                    elif i == "f":
                        i = 15
                    split.append(i)
                a = int(split[0])
                b = int(split[1])
                if mix[j][m] == "09":
                    num = mult9(a, b)
                elif mix[j][m] == "0b":
                    num = mult11(a, b)
                elif mix[j][m] == "0d":
                    num = mult13(a, b)
                else:
                    num = mult14(a, b)
                matmul.append("{0:08b}".format(int(num, 16)))
            result1 = xor(matmul[0], matmul[1])
            result2 = xor(result1, matmul[2])
            result = xor(result2, matmul[3])
            mix_c.append("{0:02x}".format(int(result, 2)))
            matmul = []

    return mix_c


def transcription(m):
    """This transcript the message from hexadecimal"""
    message = [m[0], m[4], m[8], m[12], m[1], m[5], m[9], m[13], m[2], m[6], m[10], m[14], m[3], m[7], m[11], m[15]]
    output_message = ""
    for i in message:
        a = int(i, 16)
        b = chr(a)
        output_message = output_message + b
    return output_message

