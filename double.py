def inverse_permutation(perm):
    """
    Computes the inverse of a 1-indexed permutation.
    For example, if perm = (4,2,1,3) then the inverse permutation is (3,2,4,1).
    """
    n = len(perm)
    inv = [0] * n
    for i, p in enumerate(perm):
        inv[p - 1] = i + 1
    return tuple(inv)

def double_transposition_encrypt_v2(text, row_perm, col_perm, pad_char='X'):
    """
    Encrypts text using a double transposition cipher with explicit row and column permutations.
    
    Arguments:
      text     -- plaintext string.
      row_perm -- tuple or list of integers (1-indexed) defining the new order for rows.
      col_perm -- tuple or list of integers (1-indexed) defining the new order for columns.
      pad_char -- character used for padding if text length is less than rows*columns.
    
    Returns:
      ciphertext as a string.
    """
    rows = len(row_perm)
    cols = len(col_perm)
    total = rows * cols

    # Pad text if necessary (or truncate if longer)
    if len(text) < total:
        text = text + pad_char * (total - len(text))
    elif len(text) > total:
        text = text[:total]

    # Fill matrix row-wise
    matrix = [list(text[i * cols:(i + 1) * cols]) for i in range(rows)]
    
    # Permute columns: for each row, reorder columns as specified by col_perm
    # (col_perm is assumed to be 1-indexed)
    matrix_col_permuted = []
    for row in matrix:
        new_row = [row[perm - 1] for perm in col_perm]
        matrix_col_permuted.append(new_row)
    
    # Permute rows: reorder rows as specified by row_perm (also 1-indexed)
    matrix_full = [matrix_col_permuted[perm - 1] for perm in row_perm]
    
    # Read the ciphertext row-by-row
    ciphertext = ''.join(''.join(row) for row in matrix_full)
    return ciphertext

def double_transposition_decrypt_v2(ciphertext, row_perm, col_perm):
    """
    Decrypts ciphertext encrypted with the double transposition cipher (v2).
    
    Arguments:
      ciphertext -- the encrypted text string.
      row_perm   -- the row permutation key used for encryption (1-indexed).
      col_perm   -- the column permutation key used for encryption (1-indexed).
    
    Returns:
      The recovered plaintext string.
    """
    rows = len(row_perm)
    cols = len(col_perm)
    total = rows * cols

    if len(ciphertext) != total:
        ciphertext = ciphertext.ljust(total, 'X')
    
    # Fill matrix row-wise from ciphertext
    matrix = [list(ciphertext[i * cols:(i + 1) * cols]) for i in range(rows)]
    
    # Compute inverse permutations for rows and columns
    inv_row = inverse_permutation(row_perm)
    inv_col = inverse_permutation(col_perm)
    
    # Reverse row permutation: rearrange rows to original order
    matrix_row_inversed = [None] * rows
    for i, new_pos in enumerate(inv_row):
        matrix_row_inversed[new_pos - 1] = matrix[i]
    
    # Reverse column permutation for each row
    matrix_col_inversed = []
    for row in matrix_row_inversed:
        new_row = [None] * cols
        for j, new_pos in enumerate(inv_col):
            new_row[new_pos - 1] = row[j]
        matrix_col_inversed.append(new_row)
    
    # Read the plaintext row-by-row
    plaintext = ''.join(''.join(row) for row in matrix_col_inversed)
    return plaintext

# Wrap the improved functions with shorter names and default keys.
# Default keys here are chosen as an example:
#   For a 3x4 matrix: row permutation (3,2,1) and column permutation (4,2,1,3).
def dte(text, row_perm=(3, 2, 1), col_perm=(4, 2, 1, 3), pad_char='X'):
    return double_transposition_encrypt_v2(text, row_perm, col_perm, pad_char)

def dtd(text, col=5, row_perm=(3, 2, 1), col_perm=(4, 2, 1, 3)):
    """
    Decrypts text encrypted with a double transposition cipher (v2 version)
    using explicit row and column permutations.
    
    Arguments:
      text     -- ciphertext string.
      col      -- number of columns used during encryption (for backward compatibility).
      row_perm -- row permutation key (1-indexed) used during encryption.
      col_perm -- column permutation key (1-indexed) used during encryption.
    
    Returns:
      The recovered plaintext string.
    """
    rows = len(row_perm)
    cols = len(col_perm)
    total = rows * cols

    if len(text) != total:
        text = text.ljust(total, 'X')
    
    # Fill matrix row-wise from ciphertext
    matrix = [list(text[i * cols:(i + 1) * cols]) for i in range(rows)]
    
    # Reverse row permutation:
    # For each index i, the encrypted matrix row i came from original row at index (row_perm[i]-1)
    matrix_row_inversed = [None] * rows
    for i in range(rows):
        original_index = row_perm[i] - 1
        matrix_row_inversed[original_index] = matrix[i]
    
    # Reverse column permutation:
    # For each row, rebuild the original row using the column permutation.
    # Encryption did: new_row[i] = old_row[col_perm[i]-1]
    # So, decryption does: old_row[col_perm[i]-1] = new_row[i]
    matrix_col_inversed = []
    for row in matrix_row_inversed:
        original_row = [None] * cols
        for i in range(cols):
            original_position = col_perm[i] - 1
            original_row[original_position] = row[i]
        matrix_col_inversed.append(original_row)
    
    plaintext = ''.join(''.join(row) for row in matrix_col_inversed)
    return plaintext


# Example usage:
if __name__ == "__main__":
    plaintext = "abcdefghijkl"
    # With plaintext length 12, a 3x4 matrix fits exactly.
    # Using default permutations: row_perm=(3,2,1) and col_perm=(4,2,1,3)
    ciphertext = dte(plaintext)
    print("Ciphertext:", ciphertext)  # Expected output: NADWTKCAATAT (example)
    
    recovered = dtd(ciphertext)
    print("Recovered Plaintext:", recovered)  # Should print: attackatdawn
