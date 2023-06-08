from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import sys
import hashing
import formatting
import usersDB
import logging

class MyRequestHandler (BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Content-Length")
        self.end_headers()
        return

    def do_POST(self):
        if self.path == "/defaults":
            i = 0
            self.encryptDefault()
        elif self.path == "/customs":
            self.encryptCustom()
        else:
            self.send404()
        return

    def do_GET(self):
        if self.path == "/specifications":
            self.retrieveCollection()
        else:
            self.send404()
        return

    def encryptDefault(self):
        logging.info("encrypting default password")
        length = int(self.headers["Content-Length"])

        # Retrieve data:
        body = self.rfile.read(length).decode("utf-8")
        parsedBody = parse_qs(body)
        
        # Gather data:
        try:
            if parsedBody["username"] and parsedBody["password"] and parsedBody["domain"] and parsedBody["counter"]:
                username = parsedBody["username"][0]
                password = parsedBody["password"][0]
                domain = parsedBody["domain"][0]
                counter = parsedBody["counter"][0]
        except Exception as err:
            logging.info("username, password, domain, and counter all must be Non-Empty: %s", err)
            self.send400()
            return

        # Custom salt
        salt = username + domain + counter
        try:
            finalPassword = hashing.encrypt(password, salt)
            
            # now we will check if the user needs to be added to the database
            self.checkDatabase(username, domain, counter, -1, "", None, None, None)
        except Exception as err:
            logging.info(err)
            self.send400()
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.sendPassword(finalPassword)
        return

    def sendPassword(self, encryptedPassword):
        encryptedJSON = {}
        encryptedJSON["encryptedPassword"] = encryptedPassword
        intoBytes = bytes(json.dumps(encryptedJSON), "utf-8")
        self.wfile.write(intoBytes)
        return

    def encryptCustom(self):
        logging.info("encrypting custom password")
        length = int(self.headers["Content-Length"])

        # Retrieve data:
        body = self.rfile.read(length).decode("utf-8")
        parsedBody = parse_qs(body)
        
        # Gather data:
        username = parsedBody["username"][0]
        password = parsedBody["password"][0]
        domain = parsedBody["domain"][0]
        counter = parsedBody["counter"][0]
        passwordLength = parsedBody["length"][0]
        symbols = parsedBody["symbols"][0]
        uppercase = parsedBody["uppercase"][0]
        lowercase = parsedBody["lowercase"][0]
        numbers = parsedBody["numbers"][0]

        # allowing for no given length or symbols
        if passwordLength == "default":
            pass
        elif int(passwordLength) > 0:
            passwordLength = int(passwordLength)
        else:
            logging.info("password length must be a positive integer")
            self.send400()
            return

        #passing a empty string so the alphabet doesn't mess up and we can still check.
        # if symbols == "default":
        #     symbols = ""

        if (uppercase == "true"):
            uppercase = True
        else:
            uppercase = False
        if (lowercase == "true"):
            lowercase = True
        else:
            lowercase = False
        if (numbers == "true"):
            numbers = True
        else:
            numbers = False

        salt = username + domain + counter

        try:
            encryptedPassword = hashing.encrypt(password, salt)
            finishedPassword = formatting.formatAsCustom(encryptedPassword, passwordLength, symbols, numbers, uppercase, lowercase)

            self.checkDatabase(username, domain, counter, passwordLength, symbols, uppercase, lowercase, numbers)
        except Exception as err:
            logging.info(err)
            self.send400()
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.sendPassword(finishedPassword)
        return

    def checkDatabase(self, username, domain, counter, passwordLength, symbols, uppercase, lowercase, numbers):
        db = usersDB.Users()
        result = db.getUserByUsername(username)
        needToAdd = True
        for r in result:
            if (r["username"] == username) and (r["domain"] == domain) and (r["count"] == counter) and (r["length"] == passwordLength) and (r["symbols"] == symbols) and (r["uppercase"] == uppercase) and (r["lowercase"] == lowercase) and (r["numbers"] == numbers):
                needToAdd = False
        if needToAdd:
            db.addUser(username, domain, counter, passwordLength, symbols, uppercase, lowercase, numbers)
            logging.info("Added user")
        return

    def retrieveCollection(self):
        logging.info("retrieving Collection")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        db = usersDB.Users()
        allSpecifications = db.getAllUsers()

        self.wfile.write(bytes(json.dumps(allSpecifications), "utf-8"))
        return

    # def checkRegistrations(self):
    #     logging.info(self.headers)
    #     length = int(self.headers["Content-Length"])
    #     body = self.rfile.read(length).decode("utf-8")
    #     logging.info("Body:", body)
    #     parsedBody = parse_qs(body)
    #     logging.info("Parsed Body:", parsedBody)
    #     username = parsedBody["username"][0]
    #     password = parsedBody["password"][0]
    #     firstName = parsedBody["firstName"][0]
    #     lastName = parsedBody["lastName"][0]
        
    #     db = characters_db.Users()
    #     Uid = db.getUserByUsername(username)
    #     if Uid == None:
    #         password = bcrypt.hash(password)
    #         db.addUser(username, password, firstName, lastName)
    #         self.send_response(200)
    #         self.end_headers()
    #         logging.info("Uid:", Uid)
    #         self.session["userId"] = Uid["id"]
    #         #might want to change previous line to:
    #         #self.session["userId"] = db.getUserByUsername(username)["id"]
    #     else:
    #         self.send422()

    #     #need help to figure out how to register:
    #     return

    # def checkLogins(self):
    #     logging.info(self.headers)
    #     length = int(self.headers["Content-Length"])
    #     body = self.rfile.read(length).decode("utf-8")
    #     logging.info("Body:", body)
    #     parsedBody = parse_qs(body)
    #     logging.info("Parsed Body:", parsedBody)
    #     username = parsedBody["username"][0]
    #     password = parsedBody["password"][0]
    #     db = characters_db.Users()
    #     user = db.getUserByUsername(username)
    #     if user != None:
    #         logging.info("User:", user)
    #         hashed = user["password"]
    #         if bcrypt.verify(password, hashed):
    #             self.send_response(200)
    #             self.end_headers()
    #             logging.info("Uid:", user)
    #             self.session["userId"] = user["id"]
    #         else:
    #             self.send401()
    #     else:
    #         self.send401()
    #     return

    def end_headers(self):
        # self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)
        return

    def send400(self):
        self.send_response(400)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Bad Request", "utf-8"))
        return

    def send401(self):
        self.send_response(401)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not logged in", "utf-8"))
        return

    def send404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))
        return

    def send422(self):
        self.send_response(422)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Email exists", "utf-8"))
        return



def main():
    logging.basicConfig(filename='server.log', level=logging.INFO)
    logging.info('Starting server')

    db = usersDB.Users()
    db.createTable()
    db = None # disconnect

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyRequestHandler)

    logging.info("Server listening on {}:{}".format(*listen))
    server.serve_forever()

if __name__ == '__main__':
    main()