def encrypt_caesar(plaintext):
    """
       Encrypts plaintext using a Caesar cipher.
       >>> encrypt_caesar("PYTHON")
       'SBWKRQ'
       >>> encrypt_caesar("python")
       'sbwkrq'
       >>> encrypt_caesar("Python3.6")
       'Sbwkrq3.6'
       >>> encrypt_caesar("")
       ''
       """
    cipher_text = ''
    key_shift = int(input())        # запрашиваем произвольный сдвиг
    for char in plaintext:
        if ord('A') <= ord(char) <= ord('Z'):      # проверка диапазона для заглавных символов.
            new_char = ord(char) + key_shift
            new_char = chr((new_char - ord('A')) % (ord('Z') - ord('A') + 1) + ord('A'))
            cipher_text += new_char
        elif ord('a') <= ord(char) <= ord('z'):    # проверка диапазона для малых символов
            new_char = ord(char) + key_shift
            new_char = chr((new_char - ord('a')) % (ord('z') - ord('a') + 1) + ord('a'))
            cipher_text += new_char
        else:
            cipher_text += char # для символов не английского алфавита.
    return cipher_text


def decrypt_caesar(ciphertext):
    """
        >>> decrypt_caesar("SBWKRQ")
        'PYTHON'
        >>> decrypt_caesar("sbwkrq")
        'python'
        >>> decrypt_caesar("Sbwkrq3.6")
        'Python3.6'
        >>> decrypt_caesar("")
        ''
        """
    cipher_text = ''
    key_shift = int(input())       # запрашиваем произвольный сдвиг
    for char in ciphertext:
        if ord('A') <= ord(char) <= ord('Z'):               # проверка диапазона заглвынх букв
            new_char = ord(char) - key_shift
            new_char = chr((new_char - ord('A')) % (ord('Z') - ord('A') + 1) + ord('A'))
            cipher_text += new_char
        elif ord('a') <= ord(char) <= ord('z'):             # проверка диапазона для малых букв
            new_char = ord(char) - key_shift
            new_char = chr((new_char - ord('a')) % (ord('z') - ord('a') + 1) + ord('a'))
            cipher_text += new_char
        else:
            cipher_text += char                              # в случае для символов не английского алфавита
    return cipher_text
