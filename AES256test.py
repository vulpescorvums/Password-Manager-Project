import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def generate_key():
    return get_random_bytes(32)

def generate_iv():
    return get_random_bytes(16)

def AES_encrypt(plaintext, key, iv):
    # Create a new AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Check if plaintext is not already a bytes object
    if not isinstance(plaintext, bytes):
        plaintext = plaintext.encode()

    # Pad the plaintext
    padded_plaintext = pad(plaintext, AES.block_size)

    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)

    # Encode the ciphertext as a base64 string
    ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')

    # Return the ciphertext
    return ciphertext_base64

def AES_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(base64.b64decode(ciphertext)), AES.block_size)
    return plaintext.decode('utf-8')

# def main():
#     key = generate_key()
#     iv = generate_iv()

#     print("Key:", key)
#     print("IV:", iv)

#     plaintext = "test@mail.com"
#     print("Plaintext:", plaintext)

#     ciphertext = AES_encrypt(plaintext, key, iv)
#     print("Ciphertext:", ciphertext)

#     decrypted_text = AES_decrypt(ciphertext, key, iv)
#     print("Decrypted text:", decrypted_text)

# if __name__ == "__main__":
#     main()