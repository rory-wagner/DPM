from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import sys
import hashing
import formatting
import usersDB


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
            # self.end_headers()
        elif self.path == "/customs":
            self.encryptCustom()
        else:
            self.send404()
        return

#Here I start the implementation:

    def encryptDefault(self):
        print(self.headers)
        length = int(self.headers["Content-Length"])

        # Retrieve data:
        body = self.rfile.read(length).decode("utf-8")
        print("Body:", body)
        parsedBody = parse_qs(body)
        print("Parsed Body:", parsedBody)
        
        # Gather data:
        username = parsedBody["username"][0]
        password = parsedBody["password"][0]
        website = parsedBody["website"][0]
        counter = parsedBody["counter"][0]

        print(parsedBody["username"][0])
        print(parsedBody["password"][0])
        print(parsedBody["website"][0])
        print(parsedBody["counter"][0])

        salt = username + website + counter

        #here I need to hash the salt probably with sha256 before passing it in

        encryptedPassword = hashing.encrypt(password, salt)

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.sendPassword(encryptedPassword)


        return

    def sendPassword(self, encryptedPassword):
        encryptedJSON = {}
        encryptedJSON["encryptedPassword"] = encryptedPassword
        intoBytes = bytes(json.dumps(encryptedJSON), "utf-8")
        self.wfile.write(intoBytes)
        return
    

    def encryptCustom(self):
        print(self.headers)
        length = int(self.headers["Content-Length"])

        # Retrieve data:
        body = self.rfile.read(length).decode("utf-8")
        print("Body:", body)
        parsedBody = parse_qs(body)
        print("Parsed Body:", parsedBody)
        
        # Gather data:
        username = parsedBody["username"][0]
        password = parsedBody["password"][0]
        website = parsedBody["website"][0]
        counter = parsedBody["counter"][0]
        length = parsedBody["length"][0]
        symbols = parsedBody["symbols"][0]
        uppercase = parsedBody["uppercase"][0]
        lowercase = parsedBody["lowercase"][0]
        numbers = parsedBody["numbers"][0]

        length = int(length)
        # symbols = 
        uppercase = bool(uppercase)
        lowercase = bool(lowercase)
        numbers = bool(numbers)

        print(username)
        print(password)
        print(website)
        print(counter)
        print(length)
        print(symbols)
        print(uppercase)
        print(lowercase)
        print(numbers)

        salt = username + website + counter

        encryptedPassword = hashing.encrypt(password, salt)
        finishedPassword = formatting.formatAsCustom(encryptedPassword, length, symbols, numbers, uppercase, lowercase)

        print("finished:")
        print(finishedPassword)
        print(len(finishedPassword))

        self.send_response(201)
        self.end_headers()
        self.sendPassword(finishedPassword)

        return



    # def checkRegistrations(self):
    #     print(self.headers)
    #     length = int(self.headers["Content-Length"])
    #     body = self.rfile.read(length).decode("utf-8")
    #     print("Body:", body)
    #     parsedBody = parse_qs(body)
    #     print("Parsed Body:", parsedBody)
    #     username = parsedBody["username"][0]
    #     password = parsedBody["password"][0]
    #     firstName = parsedBody["firstName"][0]
    #     lastName = parsedBody["lastName"][0]
        
    #     db = characters_db.Users()
    #     Uid = db.getUserByUsername(username)
    #     if Uid == None:
    #         password = bcrypt.hash(password)
    #         db.addUser(username, password, firstName, lastName)
    #         self.send_response(201)
    #         self.end_headers()
    #         print("Uid:", Uid)
    #         self.session["userId"] = Uid["id"]
    #         #might want to change previous line to:
    #         #self.session["userId"] = db.getUserByUsername(username)["id"]
    #     else:
    #         self.send422()

    #     #need help to figure out how to register:
    #     return

    # def checkLogins(self):
    #     print(self.headers)
    #     length = int(self.headers["Content-Length"])
    #     body = self.rfile.read(length).decode("utf-8")
    #     print("Body:", body)
    #     parsedBody = parse_qs(body)
    #     print("Parsed Body:", parsedBody)
    #     username = parsedBody["username"][0]
    #     password = parsedBody["password"][0]
    #     db = characters_db.Users()
    #     user = db.getUserByUsername(username)
    #     if user != None:
    #         print("User:", user)
    #         hashed = user["password"]
    #         if bcrypt.verify(password, hashed):
    #             self.send_response(201)
    #             self.end_headers()
    #             print("Uid:", user)
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

    #stuff that already works:


    def send404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))
        return
    
    def send401(self):
        self.send_response(401)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not logged in", "utf-8"))

        return

    def send422(self):
        self.send_response(422)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Email exists", "utf-8"))
        return



def run():
    db = characters_db.Users()
    db.createTable()
    db = None # disconnect

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyRequestHandler)

    print("Server listening on", "{}:{}".format(*listen))
    server.serve_forever()

run()
