

# Assignment 2 - Encryption/Decryption Program

This project is a command-line encryption and decryption tool implemented in Python. It supports multiple classical ciphers including:

- **Shift Cipher (Caesar Cipher)**
- **Permutation Cipher**
- **Simple Transposition Cipher**
- **Double Transposition Cipher**
- **Vigenère Cipher**

The program provides a user-friendly menu that allows you to choose a cipher, enter a message, and either encrypt or decrypt the text. Additionally, the project includes a set of test cases and a GitHub Actions pipeline to automatically run tests on every push or pull request.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Multiple Ciphers:** Encrypt and decrypt using different cipher techniques.
- **Customizable Keys:** Use default keys or provide your own.
- **Command-line Interface:** Simple text-based menu for easy interaction.
- **Support for Letters & Numbers:** The shift cipher handles both alphabets and numeric digits.
- **Automated Testing:** Includes unit tests using pytest.
- **CI/CD Pipeline:** GitHub Actions pipeline automatically runs tests on every push and pull request.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Assignment-2.git
   cd Assignment-2
   ```

2. **Install Python Dependencies:**

   Ensure you have Python 3.12 (or later) installed. Then install the required packages:

   ```bash
   python -m pip install --upgrade pip
   pip install pytest
   ```

---

## Usage

To run the encryption/decryption program:

1. **Launch the Program:**

   ```bash
   python Assignment2.py
   ```

2. **Follow the On-screen Menu:**

   - Choose the cipher method (Shift, Permutation, Transposition, Vigenère).
   - Decide whether to encrypt or decrypt.
   - Provide the message and, if desired, a custom key.
   - The program will display the resulting ciphertext or plaintext.

---

## Project Structure

```
Assignment-2/
├── Assignment2.py            # Main Python script with encryption/decryption functionality
├── tests/
│   ├── __init__.py           # (Optional) Makes tests a Python package
│   └── test_Assignment2.py   # Unit tests for the project
└── .github/
    └── workflows/
        └── test.yml          # GitHub Actions workflow file for running tests
```

---

## Running Tests

### **Locally:**

1. **Run All Tests:**

   ```bash
   python -m pytest tests/
   ```

2. **Run a Specific Test:**

   ```bash
   python -m pytest tests/test_Assignment2.py::test_shift_cipher
   ```

### **Via GitHub Actions:**

- Every push or pull request to the `main` branch will trigger the pipeline, which automatically runs the tests using pytest.

---

## CI/CD Pipeline

This project uses GitHub Actions to run tests automatically. The workflow is defined in `.github/workflows/test.yml`:

```yaml
name: Python Test Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set Up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest

      - name: Run Tests
        run: python -m pytest tests/
```

**Pipeline Explanation:**

- **Trigger:** Runs on every push or pull request to the `main` branch.
- **Environment:** Uses an Ubuntu runner with Python 3.12.
- **Steps:**
  - **Checkout Code:** Clones the repository.
  - **Set Up Python:** Configures the specified Python version.
  - **Install Dependencies:** Upgrades pip and installs pytest.
  - **Run Tests:** Executes `python -m pytest tests/` to run all test cases.
  
If the tests pass, the pipeline will complete successfully. Otherwise, it will report errors and block merging until issues are fixed.

---

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request with your changes. Make sure to run tests locally before submitting your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).

