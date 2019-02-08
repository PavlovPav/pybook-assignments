def encrypt_vigenere(plaintext, keyword):
    """
        >>> encrypt_vigenere("PYTHON", "A")
        'PYTHON'
        >>> encrypt_vigenere("python", "a")
        'python'
        >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
        'LXFOPVEFRNHR'
        """
    encrypted = list()
    for char in range(0, len(plaintext)):
        if plaintext[char].lower() < 'a' or plaintext[char].lower() > 'z':
            encrypted.append(plaintext[char])
            continue
        key = ord(keyword[char % len(keyword)].upper())  # подгоняем длину ключа под длину слова и извлекаем поочередно
        encrypted.append(chr(ord('A') + (ord(plaintext[char].upper()) + key) % 26))   # шифруем букву.
        if plaintext[char].islower():                    #
            encrypted[char] = encrypted[char].lower()    # Ставим соответсвие размеров символов слова и шифра.
    return ''.join(encrypted)


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    decrypted = list()
    for char in range(0, len(ciphertext)):
        if ciphertext[char].lower() < 'a' or ciphertext[char].lower() > 'z':
            decrypted.append(ciphertext[char])
            continue
        key = ord(keyword[char % len(keyword)].upper())  # подгоняем длину ключа под длину слова и извлекаем поочередно
        decrypted.append(chr(ord('A') + (ord(ciphertext[char].upper()) - key) % 26))
        if ciphertext[char].islower():                  #
            decrypted[char] = decrypted[char].lower()   # Ставим соответствие размеров символов слова и шифра.
    return ''.join(decrypted)


print(encrypt_vigenere('ATTACKATDOWN', 'LEMON'))
print(decrypt_vigenere('LXFOPVEFRNHR', 'LEMON'))