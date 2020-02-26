import random

gAlphabet = "?/:;<>@#$%^&*()-_+=|\\}{[]~`'\".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
gUpperAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
gLowerAlphabet = "abcdefghijklmnopqrstuvwxyz"

p = 0
q = 0
r = 0
n = 0
e = 0
d = 0

#needs to be passed in as raw string:
def convertFromNTo10(textToConvert):
    textToConvert.encode('unicode_escape')
    num = 0
    for i in range(len(textToConvert)):
        print(textToConvert[i])
        num = gAlphabet.index(textToConvert[i]) + (num * (len(gAlphabet)))
    return num

def convertFrom10ToN(x, builtAlphabet):
    # x = int(pow(int(chunk), self.e, self.n))
    q = int(x)
    a = []
    while q != 0:
        a.append(q % len(buildAlphabet))
        q = q // len(buildAlphabet)
    a.reverse()
    string = ''
    for item in a:
        string += str(buildAlphabet[item])

    return string

def convertFromStringToList(theString):
    theList = []
    for a in theString:
        theList.append(a)
    return theList

def convertFromListToString(theList):
    theString = ""
    for a in theList:
        theString += a
    return theString


#this is not deterministic yet:
def formatAsCustom(encryptedPassword, length, symbols, numbers, uppercase, lowercase):
    random.seed(convertFromNTo10(encryptedPassword))

    encryptedPassword = convertFromStringToList(encryptedPassword)

    #change length:
    encryptedPassword = encryptedPassword[0:length]

    #add symbol:
    needToAddSymbol = True
    randomSymbolIndex = random.randrange(0, length)
    for a in encryptedPassword:
        if a in symbols:
            needToAddSymbol = False
    if needToAddSymbol:
        encryptedPassword[randomSymbolIndex] = symbols[random.randrange(0,len(symbols))]

    #add number:
    randomNumberIndex = random.randrange(0, length)
    while randomNumberIndex == randomSymbolIndex:
        randomNumberIndex = random.randrange(0, length)

    randomNumber = str(random.randrange(0, 10))
    needToAddNumber = True
    for a in encryptedPassword:
        if a in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            needToAddNumber = False
    if needToAddNumber and numbers:
        encryptedPassword[randomNumberIndex] = randomNumber

    #add uppercase:
    randomUppercaseIndex = random.randrange(0, length)
    while randomUppercaseIndex == randomSymbolIndex or randomUppercaseIndex == randomNumberIndex:
        randomUppercaseIndex = random.randrange(0, length)

    randomUpper = gUpperAlphabet[random.randrange(0, len(gUpperAlphabet))]
    needToAddUpper = True
    print(encryptedPassword)
    for a in encryptedPassword:
        print(a)
        if a in gUpperAlphabet:
            needToAddUpper = False
    if needToAddUpper and uppercase:
        encryptedPassword[randomUppercaseIndex] = randomUpper

    #add lowercase:
    randomLowercaseIndex = random.randrange(0, length)
    while randomLowercaseIndex == randomSymbolIndex or randomLowercaseIndex == randomNumberIndex or randomLowercaseIndex == randomUppercaseIndex:
        randomLowercaseIndex = random.randrange(0, length)

    randomLower = gLowerAlphabet[random.randrange(0, len(gLowerAlphabet))]
    needToAddLower = True
    for a in encryptedPassword:
        if a in gLowerAlphabet:
            needToAddLower = False
    if needToAddLower and lowercase:
        encryptedPassword[randomLowercaseIndex] = randomLower

    encryptedPassword = convertFromListToString(encryptedPassword)

    return encryptedPassword
