from Assignment2 import shiftE  # Correct import statement


def test_shift_cipher():
    assert shiftE("Hello123", 4) == "Lipps567"
    assert shiftE("abcXYZ", 3) == "defABC"
    assert shiftE("999", 1) == "000"
    assert shiftE("Test!", 2) == "Vguv!"

