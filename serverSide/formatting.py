
gAlphabet = "?/:;<>@#$%^&*()-_+=|\\}{[]~`'\".,?!abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
gUpperAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
gLowerAlphabet = "abcdefghijklmnopqrstuvwxyz"
gNumbers = "0123456789"
gSymbols = "?/:;<>@#$%^&*()-_+=|\\}{[]~`'\".,?!"

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
        # print(textToConvert[i])
        num = gAlphabet.index(textToConvert[i]) + (num * (len(gAlphabet)))
    return num

def convertFrom10ToN(x, builtAlphabet):
    # x = int(pow(int(chunk), self.e, self.n))
    q = int(x)
    a = []
    while q != 0:
        a.append(q % len(builtAlphabet))
        q = q // len(builtAlphabet)
    a.reverse()
    string = ''
    for item in a:
        string += str(builtAlphabet[item])

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

def nextPsuedoRandNum(num, length):
    return ((num * 113) + 137) % length

def ensureInsert(toString, fromString, invalidIndeces):

    return toString


#this is not deterministic yet:
def formatAsCustom(encryptedPassword, length, symbols, numbers, uppercase, lowercase):
    num = convertFromNTo10(encryptedPassword)

    encryptedPassword = convertFromStringToList(encryptedPassword)

    #change length:
    print(length)
    print("type:")
    print(type(length))
    if length != "default":
        encryptedPassword = encryptedPassword[0:length]
    else:
        length = len(encryptedPassword)

    #ensure validity of password characters:
    tempSymbols = symbols
    if symbols == "default":
        tempSymbols = gSymbols
    validAlphabet = gNumbers + gUpperAlphabet + gLowerAlphabet + tempSymbols

    randNum = nextPsuedoRandNum(num, len(validAlphabet))

    for i in range(len(encryptedPassword)):
        if encryptedPassword[i] not in validAlphabet:
            randNum = nextPsuedoRandNum(randNum, len(validAlphabet))
            print(randNum)
            encryptedPassword[i] = validAlphabet[randNum]

    #add symbol:
    randSymbolIndex = nextPsuedoRandNum(randNum, length)
    randNum = nextPsuedoRandNum(randSymbolIndex, len(symbols))
    needToAddSymbol = True
    if symbols != "default":
        for a in encryptedPassword:
            if a in symbols:
                needToAddSymbol = False
        if needToAddSymbol:
            encryptedPassword[randSymbolIndex] = symbols[randNum]

    #add number:
    randNumIndex = nextPsuedoRandNum(randNum, length)
    randNum = nextPsuedoRandNum(randNumIndex, 10)
    while randNumIndex == randSymbolIndex:
        randNumIndex = nextPsuedoRandNum(randNumIndex, length)

    randomNumber = randNum % 10
    needToAddNumber = True
    for a in encryptedPassword:
        if a in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            needToAddNumber = False
    if needToAddNumber and numbers:
        encryptedPassword[randNumIndex] = str(randomNumber)

    #add uppercase:
    randUpperIndex = nextPsuedoRandNum(randNum, length)
    randNum = nextPsuedoRandNum(randUpperIndex, len(gUpperAlphabet))
    while randUpperIndex == randSymbolIndex or randUpperIndex == randNumIndex:
        randUpperIndex = nextPsuedoRandNum(randUpperIndex, length)

    randomUpper = gUpperAlphabet[randNum]
    needToAddUpper = True
    print(encryptedPassword)
    for a in encryptedPassword:
        print(a)
        if a in gUpperAlphabet:
            needToAddUpper = False
    if needToAddUpper and uppercase:
        encryptedPassword[randUpperIndex] = randomUpper

    #add lowercase:
    randLowerIndex = nextPsuedoRandNum(randNum, length)
    randNum = nextPsuedoRandNum(randLowerIndex, len(gLowerAlphabet))
    while randLowerIndex == randSymbolIndex or randLowerIndex == randNumIndex or randLowerIndex == randUpperIndex:
        randLowerIndex = nextPsuedoRandNum(randLowerIndex, length)

    randomLower = gLowerAlphabet[randNum]
    needToAddLower = True
    for a in encryptedPassword:
        if a in gLowerAlphabet:
            needToAddLower = False
    if needToAddLower and lowercase:
        encryptedPassword[randLowerIndex] = randomLower

    encryptedPassword = convertFromListToString(encryptedPassword)

    return encryptedPassword
