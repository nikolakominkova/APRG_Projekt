import constants as cn


def begin_key(mat_1, mat_2):
    """This add round key at the beginning of encryption."""
    mat = []
    for f in mat_2:
        for g in f:
            mat.append(g)
    xor = ""
    xored = []
    for i in range(0, 16):
        a = "{0:08b}".format(int(mat_1[i], 16))
        b = "{0:08b}".format(int(mat[i], 16))
        for j in range(0, 8):
            if a[j] == b[j]:
                xor = xor + "0"
            else:
                xor = xor + "1"
        back = "{0:02x}".format(int(xor, 2))
        xored.append(back)
        xor = ""
    return xored


def sub_bytes(my_matrix):
    """This make sub-bytes operation"""
    split = []
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
    sub_b = []
    for count in range(16):
        i = int(split[count * 2])
        j = int(split[count * 2 + 1])
        sub_b.append(cn.S_BOX[i][j])
    return sub_b


def shift_rows(sub_b):
    """This make shift-rows operation after sub-bytes"""
    shift_r = [[sub_b[0], sub_b[5], sub_b[10], sub_b[15]], [sub_b[4], sub_b[9], sub_b[14], sub_b[3]], [sub_b[8], sub_b[13], sub_b[2], sub_b[7]], [sub_b[12], sub_b[1], sub_b[6], sub_b[11]]]
    return shift_r


def xor(a, b):
    """This make the XOR operation over two matrixes."""
    xor = ""
    for j in range(0, 8):
        if a[j] == b[j]:
            xor = xor + "0"
        else:
            xor = xor + "1"
    return xor


def mult3(a):
    """This is part of mix columns operation."""
    b = a
    if a[0] == "1":
        a = a[1::]
        a = a + "0"
        xor_a = xor(a, "00011011")
        xored = xor(xor_a, b)
    else:
        a = a[1::]
        a = a + "0"
        xored = xor(a, b)
    return xored


def mult2(a):
    """This is part of mix columns operation."""
    if a[0] == "1":
        a = a[1::]
        a = a + "0"
        xored = xor(a, "00011011")
    else:
        a = a[1::]
        xored = a + "0"
    return xored


def mix_columns(shift_r):
    """This make the mix columns operation."""
    mix = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    bin_mat, my_list = [], []
    mix_c = []
    for i in range(4):
        bin_mat.append([])
        for index in range(4):
            bin_mat[i].append("{0:08b}".format(int(shift_r[i][index], 16)))
    for k in bin_mat:
        for j in range(4):
            matmul = []
            for m in range(4):
                if mix[j][m] == 2:
                    num = mult2(k[m])
                elif mix[j][m] == 3:
                    num = mult3(k[m])
                else:
                    num = k[m]
                matmul.append(num)
            result1 = xor(matmul[0], matmul[1])
            result2 = xor(result1, matmul[2])
            result = xor(result2, matmul[3])
            my_list.append("{0:02x}".format(int(result, 2)))
            matmul = []
        mix_c.append(my_list)
        my_list = []
    return mix_c


def x_or(mat_1, mat_2):
    """This make the XOR operation over two matrixes."""
    xor = ""
    xored = []
    for i in range(4):
        for j in range(4):
            a = "{0:08b}".format(int(mat_1[i][j], 16))
            b = "{0:08b}".format(int(mat_2[i][j], 16))
            for en in range(0, 8):
                if a[en] == b[en]:
                    xor = xor + "0"
                else:
                    xor = xor + "1"
            back = "{0:02x}".format(int(xor, 2))
            xored.append(back)
            xor = ""
    return xored


def add_round_key(mix_c, round_key):
    """This add round key after mix columns operation."""
    result = x_or(mix_c, round_key)
    return result
