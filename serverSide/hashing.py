import hashlib
import formatting

def encrypt(password=str, salt=str):

    #make salt longer:
    while len(password + salt) < 40:
        salt *= 2

    #hash:
    m = hashlib.md5()
    fullPassAndSalt = (password + salt).encode("utf-8")
    m.update(fullPassAndSalt)
    hashedPassword = m.digest()

    #format as integer:
    decodedPassword = 0
    for b in hashedPassword:
        decodedPassword *= 256
        decodedPassword += b
    
    #format as string:
    finalPassword = formatting.convertFrom10ToN(decodedPassword, formatting.gAlphabet)
    
    return finalPassword
