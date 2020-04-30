import constants as cn


def message_check(message):
    """This return list of hex numbers and number of repeatings."""
    repeating = len(message) // 16 + 1
    rest = len(message) % 16
    if rest != 0:
        for i in range(0, 16 - rest):
            message = message + " "
    message_in_list = []
    for i in message:
        b = hex(int(ord(i))).replace("0x", "")
        message_in_list.append(b)
    return message_in_list, repeating


def divide(message):
    """This divide the message into list of 16 hex numbers and return a new list full of these 16-lists
    (quantity = number of repeatings)"""
    trans_list, rep = message_check(message)
    new_list = []
    for index in range(rep):
        work_list = []
        transcripted = []
        list1, list2, list3, list4 = [], [], [], []
        for i in range(0, 16):
            work_list.append(trans_list[0 * i])
            trans_list.pop(0)
        for num in range(0, 4):
            list1.append(work_list[num * 4])
            list2.append(work_list[num * 4 + 1])
            list3.append(work_list[num * 4 + 2])
            list4.append(work_list[num * 4 + 3])
        transcripted.extend(list1)
        transcripted.extend(list2)
        transcripted.extend(list3)
        transcripted.extend(list4)
        new_list.append(transcripted)
    return new_list, rep


def divide_list(message):
    """This returns list of 16 hex numbers a number of repeatings"""
    reps = len(message) // 32
    div_list, my_list = [], []
    for i in range(reps):
        for j in range(16):
            part = message[0] + message[1]
            message = message[2:]
            my_list.append(part)
        div_list.append(my_list)
        my_list = []
    return div_list, reps


def key_check():
    """This input a check the key."""
    key_size = input("Zadejte velikost klíče (128, 192 nebo 256 bitů): ")
    if key_size == "128":
        cipher_key = input("Zadejte heslo pro šifrování o délce 16 znaků: ")
        if len(cipher_key) != 16:
            print("Zadané heslo neodpovídá požadované délce!")
            return key_check()
        return 10, cipher_key
    elif key_size == "192":
        cipher_key = input("Zadejte heslo pro šifrování o délce 24 znaků: ")
        if len(cipher_key) != 24:
            print("Zadané heslo neodpovídá požadované délce!")
            return key_check()
        return 12, cipher_key
    elif key_size == "256":
        cipher_key = input("Zadejte heslo pro šifrování o délce 32 znaků: ")
        if len(cipher_key) != 32:
            print("Zadané heslo neodpovídá požadované délce!")
            return key_check()
        return 14, cipher_key
    else:
        print("Zadané číslo neodpovídá možnostem!")
        return key_check()


def divide_key():
    """This divide key into list."""
    rounds, cipher_key = key_check()
    cipher_list = []
    for j in cipher_key:
        a = ord(j)
        b = hex(int(a)).replace("0x", "")
        cipher_list.append(b)
    key_list = []
    reps = 0
    if rounds == 10:
        reps = 4
    elif rounds == 12:
        reps = 6
    elif rounds == 14:
        reps = 8
    for i in range(reps):
        key_list.append([])
        key_list[i].append(cipher_list[i * 4])
        key_list[i].append(cipher_list[i * 4 + 1])
        key_list[i].append(cipher_list[i * 4 + 2])
        key_list[i].append(cipher_list[i * 4 + 3])
    return key_list, rounds


def rot_word(key_list):
    """This rotate key."""
    y = key_list[-1].copy()
    x = y.pop(0)
    y.append(x)
    return y


def sub_word(key_list):
    """This make sub-word operation"""
    split = []
    rot_w = rot_word(key_list)
    for i in rot_w:
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
    sub_w = []
    for count in range(4):
        i = int(split[count * 2])
        j = int(split[count * 2 + 1])
        sub_w.append(cn.S_BOX[i][j])
    return sub_w


def sub_8(rot_w):
    """This make sub-word operation"""
    split = []
    for i in rot_w:
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
    sub_w = []
    for count in range(4):
        i = int(split[count * 2])
        j = int(split[count * 2 + 1])
        sub_w.append(cn.S_BOX[i][j])
    return sub_w


def r_con(key_list, i):
    """This adds RCON constant."""
    key = sub_word(key_list)
    xor = ""
    a = "{0:08b}".format(int(key[0], 16))
    b = "{0:08b}".format(int(cn.RCON[i], 16))
    for j in range(0, 8):
        if a[j] == b[j]:
            xor = xor + "0"
        else:
            xor = xor + "1"
    key[0] = "{0:02x}".format(int(xor, 2))
    return key


def wink(mat_1, mat_2, i):
    """This helps the key expansion."""
    wink = []
    xor = ""
    for i in range(4):
        a = "{0:08b}".format(int(mat_1[i], 16))
        b = "{0:08b}".format(int(mat_2[i], 16))
        for j in range(0, 8):
            if a[j] == b[j]:
                xor = xor + "0"
            else:
                xor = xor + "1"
        back = "{0:02x}".format(int(xor, 2))
        wink.append(back)
        xor = ""
    return wink


def key_expansion():
    """This make the key expansion process."""
    key_list, rounds = divide_key()
    if rounds == 10:
        for i in range(10):
            key_list.append(wink(r_con(key_list, i), key_list[i * 4], i))
            key_list.append(wink(key_list[i * 4 + 1], key_list[i * 4 + 4], i))
            key_list.append(wink(key_list[i * 4 + 2], key_list[i * 4 + 5], i))
            key_list.append(wink(key_list[i * 4 + 3], key_list[i * 4 + 6], i))
    if rounds == 12:
        for i in range(8):
            key_list.append(wink(r_con(key_list, i), key_list[i * 6], i))
            key_list.append(wink(key_list[i * 6 + 1], key_list[i * 6 + 6], i))
            key_list.append(wink(key_list[i * 6 + 2], key_list[i * 6 + 7], i))
            key_list.append(wink(key_list[i * 6 + 3], key_list[i * 6 + 8], i))
            key_list.append(wink(key_list[i * 6 + 4], key_list[i * 6 + 9], i))
            key_list.append(wink(key_list[i * 6 + 5], key_list[i * 6 + 10], i))
    if rounds == 14:
        for i in range(7):
            key_list.append(wink(r_con(key_list, i), key_list[i * 8], i))
            key_list.append(wink(key_list[i * 8 + 1], key_list[i * 8 + 8], i))
            key_list.append(wink(key_list[i * 8 + 2], key_list[i * 8 + 9], i))
            key_list.append(wink(key_list[i * 8 + 3], key_list[i * 8 + 10], i))
            key_list.append(wink(key_list[i * 8 + 4], sub_8(key_list[i * 8 + 11]), i))
            key_list.append(wink(key_list[i * 8 + 5], key_list[i * 8 + 12], i))
            key_list.append(wink(key_list[i * 8 + 6], key_list[i * 8 + 13], i))
            key_list.append(wink(key_list[i * 8 + 7], key_list[i * 8 + 14], i))
    return key_list, rounds
