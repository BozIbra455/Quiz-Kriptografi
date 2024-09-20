import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Fungsi untuk membuat kunci sepanjang pesan Vigenere chiper
def generate_key(message, key):
    key = list(key)
    if len(message) == len(key):
        return key
    else:
        for i in range(len(message) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

# Fungsi untuk mengenkripsi pesan Vigenere Cipher
def encrypt_vigenere(plaintext, key):
    ciphertext = []
    for i in range(len(plaintext)):
        x = (ord(plaintext[i]) + ord(key[i])) % 26
        x += ord('A')
        ciphertext.append(chr(x))
    return "".join(ciphertext)

# Fungsi untuk mendekripsi pesan Vigenere Cipher
def decrypt_vigenere(ciphertext, key):
    plaintext = []
    for i in range(len(ciphertext)):
        x = (ord(ciphertext[i]) - ord(key[i]) + 26) % 26
        x += ord('A')
        plaintext.append(chr(x))
    return "".join(plaintext)

# Playfair Cipher
def generate_playfair_key_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used_letters = set()

    for char in key:
        if char not in used_letters:
            matrix.append(char)
            used_letters.add(char)

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in used_letters:
            matrix.append(char)
            used_letters.add(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_key_matrix(key)
    plaintext = plaintext.upper().replace("J", "I")
    digraphs = []

    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i + 1] if i + 1 < len(plaintext) else 'X'
        if a == b:
            digraphs.append((a, 'X'))
            i += 1
        else:
            digraphs.append((a, b))
            i += 2

    if len(digraphs[-1]) == 1:
        digraphs[-1] = (digraphs[-1][0], 'X')

    ciphertext = ""
    for a, b in digraphs:
        ax, ay = [(ix, iy) for ix, row in enumerate(matrix) for iy, val in enumerate(row) if val == a][0]
        bx, by = [(ix, iy) for ix, row in enumerate(matrix) for iy, val in enumerate(row) if val == b][0]

        if ax == bx:
            ciphertext += matrix[ax][(ay + 1) % 5] + matrix[bx][(by + 1) % 5]
        elif ay == by:
            ciphertext += matrix[(ax + 1) % 5][ay] + matrix[(bx + 1) % 5][by]
        else:
            ciphertext += matrix[ax][by] + matrix[bx][ay]

    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_key_matrix(key)
    digraphs = [(ciphertext[i], ciphertext[i + 1]) for i in range(0, len(ciphertext), 2)]

    plaintext = ""
    for a, b in digraphs:
        ax, ay = [(ix, iy) for ix, row in enumerate(matrix) for iy, val in enumerate(row) if val == a][0]
        bx, by = [(ix, iy) for ix, row in enumerate(matrix) for iy, val in enumerate(row) if val == b][0]

        if ax == bx:
            plaintext += matrix[ax][(ay - 1) % 5] + matrix[bx][(by - 1) % 5]
        elif ay == by:
            plaintext += matrix[(ax - 1) % 5][ay] + matrix[(bx - 1) % 5][by]
        else:
            plaintext += matrix[ax][by] + matrix[bx][ay]

    return plaintext

# Hill Cipher
def hill_encrypt(plaintext, key_matrix):
    plaintext = plaintext.upper().replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += 'X'

    plaintext_vector = [ord(char) - 65 for char in plaintext]
    ciphertext_vector = []

    for i in range(0, len(plaintext_vector), 2):
        pair = plaintext_vector[i:i + 2]
        encrypted_pair = np.dot(key_matrix, pair) % 26
        ciphertext_vector.extend(encrypted_pair)

    ciphertext = ''.join(chr(num + 65) for num in ciphertext_vector)
    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    det = int(np.round(np.linalg.det(key_matrix)))
    inv_det = pow(det, -1, 26)
    adj_matrix = np.round(np.linalg.inv(key_matrix) * det).astype(int) % 26
    inv_key_matrix = (inv_det * adj_matrix) % 26

    ciphertext_vector = [ord(char) - 65 for char in ciphertext]
    plaintext_vector = []

    for i in range(0, len(ciphertext_vector), 2):
        pair = ciphertext_vector[i:i + 2]
        decrypted_pair = np.dot(inv_key_matrix, pair) % 26
        plaintext_vector.extend(decrypted_pair)

    plaintext = ''.join(chr(num + 65) for num in plaintext_vector)
    return plaintext

# Fungsi untuk membuka file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            message = file.read()
            message_entry.delete(0, tk.END)
            message_entry.insert(0, message)

# Fungsi untuk menyimpan hasil
def save_file(result):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(result)

# Fungsi untuk mengenkripsi pesan melalui GUI
def encrypt_message():
    message = message_entry.get().upper()
    key = key_entry.get().upper()
    cipher_choice = cipher_var.get()

    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus minimal 12 karakter.")
        return

    if cipher_choice == "Vigenere Cipher":
        key = generate_key(message, key)
        result = encrypt_vigenere(message, key)
    elif cipher_choice == "Playfair Cipher":
        result = playfair_encrypt(message, key)
    elif cipher_choice == "Hill Cipher":
        key_matrix = np.array([[3, 3], [2, 5]])  # Contoh matriks kunci 2x2
        result = hill_encrypt(message, key_matrix)

    result_label.config(text=result)

# Fungsi untuk mendekripsi pesan melalui GUI
def decrypt_message():
    ciphertext = message_entry.get().upper()
    key = key_entry.get().upper()
    cipher_choice = cipher_var.get()

    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus minimal 12 karakter.")
        return

    if cipher_choice == "Vigenere Cipher":
        key = generate_key(ciphertext, key)
        result = decrypt_vigenere(ciphertext, key)
    elif cipher_choice == "Playfair Cipher":
        result = playfair_decrypt(ciphertext, key)
    elif cipher_choice == "Hill Cipher":
        key_matrix = np.array([[3, 3], [2, 5]])  # Contoh matriks kunci 2x2
        result = hill_decrypt(ciphertext, key_matrix)

    result_label.config(text=result)

# GUI Setup menggunakan Tkinter
window = tk.Tk()
window.title("Cipher Program")

# Opsi Cipher
cipher_var = tk.StringVar(value="Vigenere Cipher")
cipher_label = tk.Label(window, text="Pilih Cipher:")
cipher_label.grid(row=0, column=0)
cipher_options = ["Vigenere Cipher", "Playfair Cipher", "Hill Cipher"]
cipher_menu = tk.OptionMenu(window, cipher_var, *cipher_options)
cipher_menu.grid(row=0, column=1)

# Label dan entry untuk pesan
message_label = tk.Label(window, text="Pesan:")
message_label.grid(row=1, column=0)
message_entry = tk.Entry(window, width=50)
message_entry.grid(row=1, column=1)

# Label dan entry untuk kunci
key_label = tk.Label(window, text="Kunci (minimal 12 karakter):")
key_label.grid(row=2, column=0)
key_entry = tk.Entry(window, width=50)
key_entry.grid(row=2, column=1)

# Tombol enkripsi
encrypt_button = tk.Button(window, text="Enkripsi", command=encrypt_message)
encrypt_button.grid(row=3, column=0)

# Tombol dekripsi
decrypt_button = tk.Button(window, text="Dekripsi", command=decrypt_message)
decrypt_button.grid(row=3, column=1)

# Label untuk menampilkan hasil enkripsi/dekripsi
result_label = tk.Label(window, text="", fg="blue")
result_label.grid(row=4, column=1)

# Tombol buka file
open_button = tk.Button(window, text="Buka File", command=open_file)
open_button.grid(row=5, column=0)

# Tombol simpan hasil
save_button = tk.Button(window, text="Simpan Hasil", command=lambda: save_file(result_label.cget("text")))
save_button.grid(row=5, column=1)

window.mainloop()
