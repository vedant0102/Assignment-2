import string

###############################
#Shift Cypher
#################################





def shiftE(text, key=3):
    """
    Encrypts plaintext using a shift (Caesar) cipher.
    Default key=3 if none is provided.
    """
    dict = []
    for i in text:
        if i.isalpha():
            # Preserve case (uppercase vs. lowercase)
            offset = 65 if i.isupper() else 97
            shifted = chr((ord(i) - offset + key) % 26 + offset)
            dict.append(shifted)
        else:
            dict.append(i)
    return "".join(dict)

def shift_decrypt(ciphertext, key=3):
    """
    Decrypts ciphertext using a shift (Caesar) cipher.
    Default key=3 if none is provided.
    """
    # Decryption is just shifting in the opposite direction
    return shift_decrypt(ciphertext, -key)

def permutation_encrypt(text, key="QWERTYUIOPASDFGHJKLZXCVBNM"):
    """
    Encrypts text using a permutation substitution cipher.
    Default permutation is QWERTYUIOPASDFGHJKLZXCVBNM for letters A-Z.
    Non-alphabetic characters are left as-is.
    """
    # Create a mapping from A->key[0], B->key[1], ...
    mapping = {}
    uppercase_alphabet = string.ascii_uppercase
    key = key.upper()

    for i, letter in enumerate(uppercase_alphabet):
        mapping[letter] = key[i]  # e.g., 'A' -> 'Q', 'B' -> 'W', etc.

    ciphertext = []
    for char in text:
        if char.isalpha():
            # Check if uppercase or lowercase
            if char.isupper():
                ciphertext.append(mapping[char])
            else:
                # For lowercase, convert to uppercase for lookup, then lowercase the result
                ciphertext.append(mapping[char.upper()].lower())
        else:
            ciphertext.append(char)
    return "".join(ciphertext)

def permutation_decrypt(ciphertext, key="QWERTYUIOPASDFGHJKLZXCVBNM"):
    """
    Decrypts ciphertext using a permutation substitution cipher.
    Default permutation is QWERTYUIOPASDFGHJKLZXCVBNM.
    """
    # Build inverse mapping from key[0]->A, key[1]->B, ...
    uppercase_alphabet = string.ascii_uppercase
    key = key.upper()
    inverse_mapping = {}
    for i, letter in enumerate(key):
        inverse_mapping[letter] = uppercase_alphabet[i]  # e.g., 'Q' -> 'A'

    text = []
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                text.append(inverse_mapping[char])
            else:
                # Convert to uppercase for lookup, then lowercase the result
                text.append(inverse_mapping[char.upper()].lower())
        else:
            text.append(char)
    return "".join(text)

def simple_transposition_encrypt(text, num_cols=5):
    """
    Encrypts text by writing it row-by-row into a grid of num_cols columns,
    then reading it column-by-column.
    Default num_cols=5 if not provided.
    """
    # Remove spaces/newlines for a simpler demonstration
    text = text.replace(" ", "").replace("\n", "")
    ciphertext = []

    # Create rows
    rows = []
    for i in range(0, len(text), num_cols):
        rows.append(text[i:i+num_cols])

    # Read column-by-column
    for col in range(num_cols):
        for row in rows:
            if col < len(row):
                ciphertext.append(row[col])
    return "".join(ciphertext)

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

def double_transposition_encrypt(text, num_cols=5):
    """
    Perform simple transposition twice.
    """
    once = simple_transposition_encrypt(text, num_cols)
    return simple_transposition_encrypt(once, num_cols)

def double_transposition_decrypt(ciphertext, num_cols=5):
    """
    Decrypt the message encrypted with double_transposition_encrypt.
    """
    once = simple_transposition_decrypt(ciphertext, num_cols)
    return simple_transposition_decrypt(once, num_cols)

def vigenere_encrypt(text, key="KEY"):
    """
    Encrypts text using the Vigenère cipher.
    Default key='KEY' if not provided.
    """
    ciphertext = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            shift = ord(key[key_index % len(key)]) - 65
            encrypted_char = chr((ord(char) - offset + shift) % 26 + offset)
            ciphertext.append(encrypted_char)
            key_index += 1
        else:
            ciphertext.append(char)
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key="KEY"):
    """
    Decrypts ciphertext using the Vigenère cipher.
    """
    text = []
    key = key.upper()
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            shift = ord(key[key_index % len(key)]) - 65
            decrypted_char = chr((ord(char) - offset - shift) % 26 + offset)
            text.append(decrypted_char)
            key_index += 1
        else:
            text.append(char)
    return "".join(text)


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
        perm_key = "QWERTYUIOPASDFGHJKLZXCVBNM"
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
                        print("Invalid input. Please enter a valid integer for the shift key.")
            elif option == '2':  # Permutation Cipher
                while True:
                    user_perm = input("Enter a permutation of 26 letters (A-Z): ").upper().strip()
                    if len(user_perm) == 26 and all(letter in string.ascii_uppercase for letter in user_perm):
                        perm_key = user_perm
                        break
                    else:
                        print("Invalid permutation. Please ensure it contains exactly 26 letters (A-Z).")
            elif option in ['3', '4']:  # Simple or Double Transposition
                while True:
                    try:
                        transposition_key = int(input("Enter number of columns (integer): "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for the number of columns.")
            elif option == '5':  # Vigenère Cipher
                while True:
                    user_vigenere = input("Enter the Vigenère key (letters only): ").upper().strip()
                    if user_vigenere.isalpha():
                        vigenere_key = user_vigenere
                        break
                    else:
                        print("Invalid key. Please enter letters only.")


        if option == '1':  # Shift Cipher
            if eod == 'e':
                output = shiftE(message, shift_key)
            else:
                output = shift_decrypt(message, shift_key)

        elif option == '2':  # Permutation Cipher
            if eod == 'e':
                output = permutation_encrypt(message, perm_key)
            else:
                output = permutation_decrypt(message, perm_key)

        elif option == '3':  # Simple Transposition
            if eod == 'e':
                output = simple_transposition_encrypt(message, transposition_key)
            else:
                output = simple_transposition_decrypt(message, transposition_key)

        elif option == '4':  # Double Transposition
            if eod == 'e':
                output = double_transposition_encrypt(message, transposition_key)
            else:
                output = double_transposition_decrypt(message, transposition_key)

        elif option == '5':  # Vigenère
            if eod == 'e':
                output = vigenere_encrypt(message, vigenere_key)
            else:
                output = vigenere_decrypt(message, vigenere_key)

        # Display result
        if eod == 'e':
            print(f"\nEncrypted Message (Ciphertext): {output}")
        else:
            print(f"\nDecrypted Message (text): {output}")


if __name__ == "__main__":
    all_cipher()
