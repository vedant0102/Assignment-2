import string
from itertools import zip_longest

###############################
# Shift Cipher
#################################

def shiftE(text, key=3):
    join_arr = []
    for i in text:
        if i.isalpha():
            num = 65 if i.isupper() else 97
            answer = chr((ord(i) - num + key) % 26 + num)
            join_arr.append(answer)
        elif i.isdigit():
            num = 48 
            answer = chr((ord(i) - num + key) % 10 + num)
            join_arr.append(answer)
        else:
            join_arr.append(i)
    return "".join(join_arr)

def shiftD(text, key=3):
    return shiftE(text, -key)

###############################
# Permutation Cipher
#################################

def permutationE(text, key="PLMOKNIJBUHVYGCTFXRDZESWAQ"):
    big = string.ascii_uppercase
    key = key.upper()
    mapping = {l: key[i] for i, l in enumerate(big)}
    join_arr = [
        mapping[j.upper()] if j.isalpha() and j.isupper() 
        else (mapping[j.upper()].lower() if j.isalpha() else j)
        for j in text
    ]
    return "".join(join_arr)

def permutationD(ciphertext, key="PLMOKNIJBUHVYGCTFXRDZESWAQ"):
    uppercase_alphabet = string.ascii_uppercase
    key = key.upper()
    inverse_mapping = { letter: uppercase_alphabet[i] for i, letter in enumerate(key) }
    join_arr = [
        inverse_mapping[char] if char.isalpha() and char.isupper()
        else (inverse_mapping[char.upper()].lower() if char.isalpha() else char)
        for char in ciphertext
    ]
    return "".join(join_arr)

###############################
# Simple Transposition Encryption
#################################

def st_encrypt(text, num_cols=5):
    text = text.replace(" ", "").replace("\n", "")
    rows = [text[i:i+num_cols] for i in range(0, len(text), num_cols)]
    return "".join(letter for col in zip_longest(*rows, fillvalue="") for letter in col)

def st_decrypt(text, cols=5):
    num_rows = len(text) // cols
    remainder = len(text) % cols
    idx = 0
    columns = [''] * cols
    for col in range(cols):
        col_size = num_rows + (1 if col < remainder else 0)
        columns[col] = text[idx:idx+col_size]
        idx += col_size
    rows = zip_longest(*columns, fillvalue="")
    join_arr = [char for row in rows for char in row if char]
    return "".join(join_arr)

###############################
# Double Transposition Encryption
#################################

def double_transposition_encrypt_v2(text, row_perm, col_perm, pad_char='X'):
    rows = len(row_perm)
    cols = len(col_perm)
    total = rows * cols

    if len(text) < total:
        text = text + pad_char * (total - len(text))
    elif len(text) > total:
        text = text[:total]

    matrix = [list(text[i * cols:(i + 1) * cols]) for i in range(rows)]
    matrix_col_permuted = [[row[perm - 1] for perm in col_perm] for row in matrix]
    
    matrix_full = [matrix_col_permuted[perm - 1] for perm in row_perm]
    
    ciphertext = ''.join(''.join(row) for row in matrix_full)
    return ciphertext

def double_transposition_decrypt_v2(ciphertext, row_perm, col_perm):
    rows = len(row_perm)
    cols = len(col_perm)
    total = rows * cols

    if len(ciphertext) != total:
        ciphertext = ciphertext.ljust(total, 'X')
    
    matrix = [list(ciphertext[i * cols:(i + 1) * cols]) for i in range(rows)]
    
    matrix_row_inversed = [None] * rows
    for i in range(rows):
        original_index = row_perm[i] - 1
        matrix_row_inversed[original_index] = matrix[i]
    
    matrix_col_inversed = []
    for row in matrix_row_inversed:
        original_row = [None] * cols
        for i in range(cols):
            original_position = col_perm[i] - 1
            original_row[original_position] = row[i]
        matrix_col_inversed.append(original_row)
    
    plaintext = ''.join(''.join(row) for row in matrix_col_inversed)
    return plaintext

def dte(text, row_perm=(3, 2, 1), col_perm=(4, 2, 1, 3), pad_char='X'):
    return double_transposition_encrypt_v2(text, row_perm, col_perm, pad_char)

def dtd(text, row_perm=(3, 2, 1), col_perm=(4, 2, 1, 3)):
    return double_transposition_decrypt_v2(text, row_perm, col_perm)

###############################
# Vigenère Encryption
#################################

def ve(text, key="KEY"):
    key = key.upper()
    key_index = 0
    join_arr = []
    for i in text:
        if i.isalpha():
            offset = 65 if i.isupper() else 97
            shift = ord(key[key_index % len(key)]) - 65
            encrypted_char = chr((ord(i) - offset + shift) % 26 + offset)
            join_arr.append(encrypted_char)
            key_index += 1
        else:
            join_arr.append(i)
    return "".join(join_arr)

def vd(text, key="KEY"):
    key = key.upper()
    ind = 0
    join_arr = []
    for i in text:
        if i.isalpha():
            start = 65 if i.isupper() else 97
            shift = ord(key[ind % len(key)]) - 65
            decrypted_char = chr((ord(i) - start - shift) % 26 + start)
            join_arr.append(decrypted_char)
            ind += 1
        else:
            join_arr.append(i)
    return "".join(join_arr)

###############################
# Main Menu
#################################

def all_cipher():
    while True:
        menu_text = """
Encryption or Decryption
1. Shift Cipher
2. Permutation Cipher
3. Simple Transposition
4. Double Transposition
5. Vigenère Cipher
enter exit to quit
"""
        print(menu_text)
        valid_choices = {'1', '2', '3', '4', '5'}

        option = input("Select an option (1-5) or type 'exit' to quit: ").strip().lower()
        if option == 'exit':
            print("Exited.")
            break
        if option not in valid_choices:
            print("Invalid choice. Please try again.")
            continue

        eod = input("Press 'E' to Encrypt, 'D' to Decrypt, or 'Q' to Quit: ").strip().lower()
        if eod == 'q':
            print("Exiting...")
            break
        if eod not in ['e', 'd']:
            print("Invalid choice. Please try again.")
            continue

        message = input("Enter text to encrypt: ") if eod == 'e' else input("Enter text to decrypt: ")

        # Default keys for each cipher type
        shift_key = 3
        perm_key = "PLMOKNIJBUHVYGCTFXRDZESWAQ"
        transposition_key = 4  # used only for simple transposition
        vigenere_key = "KEY"
        # Default double transposition keys:
        row_perm_default = (3, 2, 1)
        col_perm_default = (4, 2, 1, 3)

        # Variables to hold double transposition keys (start with defaults)
        row_perm_used = row_perm_default
        col_perm_used = col_perm_default

        # Ask user if they want to provide a custom key
        custom = input("Provide a custom key? (y/n): ").strip().lower()
        if custom == 'y':
            if option == '1':  # Shift Cipher
                while True:
                    try:
                        shift_key = int(input("Enter an integer shift key: "))
                        break
                    except ValueError:
                        print("Wrong input.")
            elif option == '2':  # Permutation Cipher
                while True:
                    user_perm = input("Enter a permutation of 26 letters (A-Z): ").upper().strip()
                    if len(user_perm) == 26 and all(letter in string.ascii_uppercase for letter in user_perm):
                        perm_key = user_perm
                        break
                    else:
                        print("Invalid permutation.")
            elif option == '3':  # Simple Transposition
                while True:
                    try:
                        transposition_key = int(input("Enter number of columns (integer): "))
                        break
                    except ValueError:
                        print("Wrong input.")
            elif option == '4':  # Double Transposition
                # Prompt for both row and column permutation keys.
                row_key_input = input("Enter row permutation (comma-separated, e.g., 3,2,1): ")
                col_key_input = input("Enter column permutation (comma-separated, e.g., 4,2,1,3): ")
                try:
                    row_perm_used = tuple(int(num.strip()) for num in row_key_input.split(","))
                    col_perm_used = tuple(int(num.strip()) for num in col_key_input.split(","))
                except ValueError:
                    print("Invalid input for permutations. Using default keys.")
            elif option == '5':  # Vigenère
                while True:
                    user_vigenere = input("Enter the Vigenère key (letters only): ").upper().strip()
                    if user_vigenere.isalpha():
                        vigenere_key = user_vigenere
                        break
                    else:
                        print("Wrong key (enter letters only).")

        # Use Python's match-case to select the cipher
        match option:
            case '1':  # Shift Cipher
                output = shiftE(message, shift_key) if eod == 'e' else shiftD(message, shift_key)
            case '2':  # Permutation Cipher
                output = permutationE(message, perm_key) if eod == 'e' else permutationD(message, perm_key)
            case '3':  # Simple Transposition
                output = st_encrypt(message, transposition_key) if eod == 'e' else st_decrypt(message, transposition_key)
            case '4':  # Double Transposition (using improved v2 functions)
                output = dte(message, row_perm_used, col_perm_used) if eod == 'e' else dtd(message, row_perm_used, col_perm_used)
            case '5':  # Vigenère Cipher
                output = ve(message, vigenere_key) if eod == 'e' else vd(message, vigenere_key)
            case _:
                output = "Invalid option"

        if eod == 'e':
            print(f"\nEncrypted Message = : {output}")
        else:
            print(f"\nDecrypted Message  = : {output}")

if __name__ == "__main__":
    all_cipher()
