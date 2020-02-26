import base64
import bcrypt

def encrypt(password, salt):

    hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    hashedPassword.decode()
    hashedPassword = str(hashedPassword)
    hashedPassword = hashedPassword[9:-1]
    
    return hashedPassword
