import sys
import base64
import os
import errno
from Crypto import Random
from Crypto.Cipher import AES

BS = 16


def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def unpad(s): return s[0:-ord(s[-1])]


class AESCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = sys.argv[2]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc))


arr = os.listdir("./")

arr = [a for a in arr if ((".html" in a) or (".js") in a or (".css") in a)]


for file in arr:
    cipher = AESCipher(sys.argv[1])
    print(file)
    data = ""
    input_file = file
    with open(input_file, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    enc_input = data
    decrypted = cipher.decrypt(enc_input)
    filename = "decrypted/" + input_file
    with open(filename, "w") as f:
        f.write(decrypted)
