import inputs as inp
import encryption as enc
import decryption as dec


def option():
    """This let user choose the operation and insert the message."""
    print("Vyberte operaci:")
    print("a) šifrování zprávy")
    print("b) dešifrování zprávy")
    print("c) šifrování a následné dešifrování zprávy")
    cryption = input()
    if cryption == "a":
        message = input("Zadejte zprávu pro šifrování (bez diakritiky): ")
    elif cryption == "b":
        message = input("Zadejte zprávu pro dešifrování v hexadecimální soustavě (délka je násobkem 32!): ")
        if len(message) % 32 != 0:
            print("Zadaná délka neodpovídá násobkům 32!")
            return option()
    elif cryption == "c":
        message = input("Zadejte zprávu pro šifrování (bez diakritiky): ")
    else:
        print("Neodpovídá možnostem!")
        return option()
    return cryption, message


def encryption(message):
    """This make the encryption process."""
    message_list, repeating = inp.divide(message)
    key_list, rounds = inp.key_expansion()
    encrypted = []
    for reps in range(repeating):
        add_rk = enc.begin_key(message_list[reps], key_list[:4])
        for cycle in range(rounds - 1):
            sub_b = enc.sub_bytes(add_rk)
            shift_r = enc.shift_rows(sub_b)
            mix_c = enc.mix_columns(shift_r)
            add_rk = enc.add_round_key(mix_c, key_list[(cycle + 1) * 4:(cycle + 2) * 4])
        sub_b = enc.sub_bytes(add_rk)
        shift_r = enc.shift_rows(sub_b)
        add_rk = enc.add_round_key(shift_r, key_list[rounds * 4:(rounds + 1) * 4])
        encrypted.append(add_rk)
    return encrypted


def decryption(message):
    """This make the decryption process."""
    message, repeating = inp.divide_list(message)
    key_list, rounds = inp.key_expansion()
    output_message = ""
    if rounds == 10:
        num = 40
    elif rounds == 12:
        num = 48
    else:
        num = 56
    for reps in range(repeating):
        mix_c = enc.begin_key(message[reps], key_list[num:num + 4])
        for cycle in range(rounds - 1):
            shift_r = dec.inv_shift_rows(mix_c)
            sub_b = dec.inv_sub_bytes(shift_r)
            add_rk = enc.add_round_key(sub_b, key_list[num - ((cycle + 1) * 4):(num + 4) - ((cycle + 1) * 4)])
            mix_c = dec.inv_mix_columns(add_rk)
        shift_r = dec.inv_shift_rows(mix_c)
        sub_b = dec.inv_sub_bytes(shift_r)
        add_rk = enc.add_round_key(sub_b, key_list[num - (rounds * 4):(num + 4) - (rounds * 4)])
        output_message = output_message + dec.transcription(add_rk)
    return output_message


def enc_dec(message):
    """This make both cryption process."""
    message_list, repeating = inp.divide(message)
    key_list, rounds = inp.key_expansion()
    encrypted = []
    for reps in range(repeating):
        add_rk = enc.begin_key(message_list[reps], key_list[:4])
        for cycle in range(rounds - 1):
            sub_b = enc.sub_bytes(add_rk)
            shift_r = enc.shift_rows(sub_b)
            mix_c = enc.mix_columns(shift_r)
            add_rk = enc.add_round_key(mix_c, key_list[(cycle + 1) * 4:(cycle + 2) * 4])
        sub_b = enc.sub_bytes(add_rk)
        shift_r = enc.shift_rows(sub_b)
        add_rk = enc.add_round_key(shift_r, key_list[rounds * 4:(rounds + 1) * 4])
        encrypted.append(add_rk)
    my_message = ""
    output_message = ""
    for i in encrypted:
        for j in i:
            my_message = my_message + j
    message, repeating = inp.divide_list(my_message)
    if rounds == 10:
        num = 40
    elif rounds == 12:
        num = 48
    else:
        num = 56
    for reps in range(repeating):
        mix_c = enc.begin_key(message[reps], key_list[num:num + 4])
        for cycle in range(rounds - 1):
            shift_r = dec.inv_shift_rows(mix_c)
            sub_b = dec.inv_sub_bytes(shift_r)
            add_rk = enc.add_round_key(sub_b, key_list[num - ((cycle + 1) * 4):(num + 4) - ((cycle + 1) * 4)])
            mix_c = dec.inv_mix_columns(add_rk)
        shift_r = dec.inv_shift_rows(mix_c)
        sub_b = dec.inv_sub_bytes(shift_r)
        add_rk = enc.add_round_key(sub_b, key_list[num - (rounds * 4):(num + 4) - (rounds * 4)])
        output_message = output_message + dec.transcription(add_rk)
    return encrypted, output_message


def main():
    cryption, message = option()
    if cryption == "a":
        print("Zašifrovaná zpráva: ", encryption(message))
    elif cryption == "b":
        print("Dešifrovaná zpráva: ", decryption(message))
    elif cryption == "c":
        encrypt, decrypt = enc_dec(message)
        print("Zašifrovaná zpráva: ", encrypt)
        print("Dešifrovaná zpráva: ", decrypt)


main()
