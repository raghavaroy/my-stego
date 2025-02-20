import cv2
import os
import numpy as np

def xor_encrypt_decrypt(text, key):
    """Encrypt or decrypt text using a repeating XOR key."""
    return ''.join(chr(ord(text[i]) ^ ord(key[i % len(key)])) for i in range(len(text)))

def encode_message(img_path, output_path, msg, password):
    img = cv2.imread(img_path)
    
    if img is None:
        print("Error: Image not found!")
        return
    
    height, width, _ = img.shape
    max_chars = height * width - 2  # Reserve 2 pixels for length storage

    if len(msg) > max_chars:
        print(f"Message too long! Max length is {max_chars} characters.")
        return

    # Encrypt the message using XOR encryption
    encrypted_msg = xor_encrypt_decrypt(msg, password)
    msg_length = len(encrypted_msg)

    # Store message length in the first pixel (avoiding uint8 overflow)
    img[0, 0, 0] = np.uint8(msg_length // 256)  # High byte
    img[0, 0, 1] = np.uint8(msg_length % 256)   # Low byte

    # Store encrypted message in pixels
    n, m = 0, 2  # Start after length storage
    for i in range(msg_length):
        img[n, m, 0] = np.uint8(ord(encrypted_msg[i]))  # Store in blue channel only
        m += 1
        if m >= width:
            n += 1
            m = 0

    cv2.imwrite(output_path, img)
    print("Message encrypted successfully!")
    os.system(f"start {output_path}")

def decode_message(img_path, password):
    img = cv2.imread(img_path)

    if img is None:
        print("Error: Image not found!")
        return
    
    # Retrieve message length from the first pixel (convert to int explicitly)
    length = (int(img[0, 0, 0]) * 256) + int(img[0, 0, 1])

    encrypted_message = ""
    n, m = 0, 2  # Start after length storage
    for _ in range(length):
        encrypted_message += chr(int(img[n, m, 0]))  # Ensure correct integer conversion
        m += 1
        if m >= img.shape[1]:
            n += 1
            m = 0

    # Decrypt message
    decrypted_msg = xor_encrypt_decrypt(encrypted_message, password)
    print("Decrypted message:", decrypted_msg)

# Example Usage
img_file = "mypic.jpg"
output_file = "Encryptedmsg.png"

secret_msg = input("Enter secret message: ")
password = input("Enter password: ")

encode_message(img_file, output_file, secret_msg, password)

# Decryption
user_pass = input("Enter passcode for Decryption: ")
decode_message(output_file, user_pass)
