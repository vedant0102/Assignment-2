import string

###############################
#Shift Cypher
#################################

def shiftE(text, key=3):
    join_arr = []
    for i in text:
        if i.isalpha():
            if i.isupper():
                num = 65
            else:
                num = 97
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
#Permutation Cypher
#################################

def permutationE(text, key="PLMOKNIJBUHVYGCTFXRDZESWAQ"):
    big = string.ascii_uppercase
    key = key.upper()
    dict = {}
    for i, l in enumerate(big):
        dict[l] = key[i]
    join_arr = [
        dict[j.upper()] if j.isalpha() and j.isupper() 
        else (dict[j.upper()].lower() if j.isalpha() else j)
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
#Simple Transporation Encryption
#################################

from itertools import zip_longest
def st_encrypt(text, num_cols=5):
    text = text.replace(" ", "").replace("\n", "")
    rows = [text[i:i+num_cols] for i in range(0, len(text), num_cols)]
    return "".join(letter for col in zip_longest(*rows, fillvalue="") for letter in col)

def simple_transposition_decrypt(ciphertext, num_cols=5):
    """
    Decrypts a message encrypted with simple_transposition_encrypt.
    """
    # The number of rows is based on how many full columns we can form
    num_rows = len(ciphertext) // num_cols
    # If there's a remainder, we have an extra partial row
    remainder = len(ciphertext) % num_cols

    # We'll build the grid column-by-column
    # Each column has 'num_rows' or 'num_rows+1' characters (for columns < remainder)
    grid = [''] * num_rows
    if remainder > 0:
        grid.append('')  # For the partial row

    idx = 0
    columns = [''] * num_cols

    for col in range(num_cols):
        # Determine how many characters belong to this column
        col_size = num_rows + (1 if col < remainder else 0)
        # Extract that portion from ciphertext
        columns[col] = ciphertext[idx:idx+col_size]
        idx += col_size

    # Now read row-by-row
    text = []
    max_row = num_rows + (1 if remainder > 0 else 0)
    for r in range(max_row):
        for c in range(num_cols):
            if r < len(columns[c]):
                text.append(columns[c][r])
    return "".join(text)

###############################
#Double Transporation Encryption
#################################

def dte(text, col=5):
    once = st_encrypt(text, col)
    return st_encrypt(once, col)

def dtd(text, col=5):
    once = simple_transposition_decrypt(text, col)
    return simple_transposition_decrypt(once, col)

###############################
#Vigenere Encryption
#################################

def ve(text, key="KEY"):
    key = key.upper()
    key_index = 0
    join_arr = []
    for i in text:
        if i.isalpha():
            if i.isupper():
                offset = 65
            else:
                offset = 97
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
            if i.isupper():
                start = 65
            else:
                start = 97
            shift = ord(key[ind % len(key)]) - 65
            decrypted_char = chr((ord(i) - start - shift) % 26 + start)
            join_arr.append(decrypted_char)
            ind += 1
        else:
            join_arr.append(i)
    return "".join(join_arr)


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

        while True:
            option = input("Select an option (1-5) or type 'exit' to quit: ").strip().lower()

            if option == 'exit':
                print("Exited.")
                break
            if option in valid_choices:
                print(f"You selected option {option}.")
                break
            else:
                print("Invalid choice. Please try again.")


        while True:
            eod = input("Press 'E' to Encrypt, 'D' to Decrypt, or 'Q' to Quit: ").strip().lower()

            if eod == 'e':
                message = input("Enter text to encrypt: ")
                break 
            elif eod == 'd':
                message = input("Enter text to decrypt: ")
                break  
            elif eod == 'q':
                print("Exiting...")
                exit()
            else:
                print("Invalid choice. Please enter 'E' for Encrypt, 'D' for Decrypt, or 'Q' to Quit.")



        # Default keys for each cipher type
        shift_key = 7
        perm_key = "PLMOKNIJBUHVYGCTFXRDZESWAQ"
        transposition_key = 4
        vigenere_key = "KEY"

        # Ask the user if they want to provide a custom key
        key = input("provide a key? (y/n): ").strip().lower()

        if key == 'y':
            if option == '1':  # Shift Cipher
                while True:
                    try:
                        shift_key = int(input("Enter an integer shift key: "))
                        break
                    except ValueError:
                        print("Wrong input.")
            elif option == '2': 
                while True:
                    user_perm = input("Enter a permutation of 26 letters (A-Z): ").upper().strip()
                    if len(user_perm) == 26 and all(letter in string.ascii_uppercase for letter in user_perm):
                        perm_key = user_perm
                        break
                    else:
                        print("Invalid permutation.")
            elif option in ['3', '4']:
                while True:
                    try:
                        transposition_key = int(input("Enter number of columns (integer): "))
                        break
                    except ValueError:
                        print("Wrong Input")
            elif option == '5': 
                while True:
                    user_vigenere = input("Enter the Vigenère key (letters only): ").upper().strip()
                    if user_vigenere.isalpha():
                        vigenere_key = user_vigenere
                        break
                    else:
                        print("Wrong key. (enter letters)")


        match option:
            case '1':  # Shift Cipher
                output = shiftE(message, shift_key) if eod == 'e' else shiftD(message, shift_key)
            case '2':  # Permutation Cipher
                output = permutationE(message, perm_key) if eod == 'e' else permutationD(message, perm_key)
            case '3':  # Simple Transposition
                output = st_encrypt(message, transposition_key) if eod == 'e' else simple_transposition_decrypt(message, transposition_key)
            case '4':  # Double Transposition
                output = dte(message, transposition_key) if eod == 'e' else dtd(message, transposition_key)
            case '5':  # Vigenère
                output = ve(message, vigenere_key) if eod == 'e' else vd(message, vigenere_key)
            case _:
                output = "Invalid option"


        # Display result
        if eod == 'e':
            print(f"\nEncrypted Message = : {output}")
        else:
            print(f"\nDecrypted Message  = : {output}")


if __name__ == "__main__":
    all_cipher()
