import string
import pytest
from Assignment2 import (
    shiftE,
    shiftD,
    permutationE,
    permutationD,
    simple_transposition_encrypt,
    simple_transposition_decrypt,
    dte,
    dtd,
    vigenere_encrypt,
    vigenere_decrypt,
)

###############################
# Shift Cipher Tests
###############################

def test_shift_cipher_encryption():
    # Test encryption using shiftE with various inputs
    assert shiftE("Hello123", 4) == "Lipps567"
    assert shiftE("abcXYZ", 3) == "defABC"
    assert shiftE("999", 1) == "000"
    assert shiftE("Test!", 2) == "Vguv!"

def test_shift_cipher_decryption():
    # Decrypt the previously encrypted text to recover the original message
    original = "Hello123"
    encrypted = shiftE(original, 4)
    assert shiftD(encrypted, 4) == original

    original = "abcXYZ"
    encrypted = shiftE(original, 3)
    assert shiftD(encrypted, 3) == original

###############################
# Permutation Cipher Tests
###############################

def test_permutation_cipher_encryption():
    key = "PLMOKNIJBUHVYGCTFXRDZESWAQ"
    # For uppercase text
    original_upper = "HELLO"
    expected_upper = "".join([key[ord(c)-65] for c in original_upper])
    assert permutationE(original_upper, key) == expected_upper

    # For lowercase text, mapping should preserve case.
    original_lower = "hello"
    expected_lower = "".join([key[ord(c)-97].lower() for c in original_lower])
    assert permutationE(original_lower, key) == expected_lower

def test_permutation_cipher_decryption():
    key = "PLMOKNIJBUHVYGCTFXRDZESWAQ"
    original = "HELLO"
    encrypted = permutationE(original, key)
    decrypted = permutationD(encrypted, key)
    assert decrypted == original

    original = "hello"
    encrypted = permutationE(original, key)
    decrypted = permutationD(encrypted, key)
    assert decrypted == original

###############################
# Simple Transposition Tests
###############################

def test_simple_transposition_encrypt_decrypt():
    # Using a sentence with spaces which are removed in encryption.
    text = "WE ARE DISCOVERED FLEE AT ONCE"
    encrypted = simple_transposition_encrypt(text, num_cols=5)
    decrypted = simple_transposition_decrypt(encrypted, num_cols=5)
    # The encryption function removes spaces and newlines,
    # so we compare against the stripped version.
    expected = text.replace(" ", "").replace("\n", "")
    assert decrypted == expected

###############################
# Double Transposition Tests
###############################

def test_double_transposition_encrypt_decrypt():
    text = "WEAREDISCOVEREDFLEEATONCE"
    encrypted = dte(text, num_cols=4)
    decrypted = dtd(encrypted, num_cols=4)
    assert decrypted == text

###############################
# Vigenère Cipher Tests
###############################

def test_vigenere_encrypt_decrypt_upper():
    text = "ATTACKATDAWN"
    key = "LEMON"
    encrypted = vigenere_encrypt(text, key)
    decrypted = vigenere_decrypt(encrypted, key)
    assert decrypted == text

def test_vigenere_encrypt_decrypt_mixed():
    text = "Attack at dawn!"
    key = "LEMON"
    encrypted = vigenere_encrypt(text, key)
    decrypted = vigenere_decrypt(encrypted, key)
    assert decrypted == text
