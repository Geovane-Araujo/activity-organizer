import string
import random
import base64

def encode():
    token = ""
    for x in range(1):
        token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
    return token