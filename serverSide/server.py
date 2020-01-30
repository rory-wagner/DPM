from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import sys
import argon2

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
        elif self.path == "/logins":
            self.checkLogins()
        elif self.path == "/registrations":
            self.checkRegistrations()
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

        salt = "saltGoHere"

        encryptedPassword = self.encrypt(password, salt)

        finishedPassword = self.formatAsDefault(encryptedPassword)

        self.send_response(201)
        self.end_headers()

        return
    
    def formatAsDefault(self, encryptedPassword):

        return

    def encrypt(self, password, salt):
    #notes:

    #check this for salting and such:
    # https://passlib.readthedocs.io/en/stable/lib/passlib.hash.argon2.html

    # >>> import argon2
    # >>> argon2.argon2_hash("password", "some_salt", )
    # b'\xa8&x\xc7\xd9\xc4\x1f\xdf[2\xd9hq\xab\xe5\xb4WV\x89\xca\xa4\xee\xb3\x98\xf1I\xd1\xdaf\xe7=\xfaA\x04\xeb\xe1\xfd\x94)\xad\x84\r\x9ed<8xE\xc3\xd3\xfb\x13\xcbN\xcf\\}\xfd-9\x8b\x07@\xd8\x10\x1a\x83\x05\xd5\xfd\xc4m\x9f\xd7\x81\xdcX\x87\xb2\x02\xa9R\xc1\x9d\xaf6\xbb\x8c\xe1vH+\x07\xc7Y\x80\xb3\xb5\xf8\xba\xbd\x87\xd8\xf5\xea\x1a\x04V&\xf7\xde\x9b\x93\x8dbQ\x91e\xf6\xd6\xa2\xd8G8\xe3\x9a\x03\xf3'
    # _________________________________________________________________________________________________
    # >>> import argon2
    # >>> argon2.argon2_hash(password="some password", salt="some salt", t=16, m=8, p=1, buflen=128, argon_type=argon2.Argon2Type.Argon2_i)
    # b"\x1f>\xe0\xb8\x88%\xef\xee\xb3n\\\xb85\x03\x14\xb8\xb8O\x02Zk\xbf<\xd5\xa0C\xf2,p\x00\xda\xd7Bc\xa71\x84\x10\x00\x8cx'\xec?Q\x8499\x9b\xd4)\xf1\x98F\x13!\x8bB\x12!\xc3U\x8d\x9a\xb5\x10\x8cIo\xd2p\xcd'\x8c\x96d\xa5?{\x1d*\xaf\xab\x99\x9e\xe9c\xa4\xb7\xb2\x00\xfa\x82\x96/\xdei_1Nun\x92j\n\xf3D#\x05\tj\xa2\x92\xd5\xf4nym\xd1Kq\xa1|\xd19\xa9Q8"

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
    # db = characters_db.CharactersDB()
    # db.createTable()
    # db = None # disconnect
    # db = characters_db.Users()
    # db.createTable()
    # db = None # disconnect

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyRequestHandler)

    print("Server listening on", "{}:{}".format(*listen))
    server.serve_forever()

run()
