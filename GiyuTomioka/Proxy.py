from Encryption import EncryptionHandler
import socket
import threading 


class Interface:
	def __init__(self):
		self.host = '127.0.0.1' #localhost
        self.port = 50222
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.connected = 0
        self.pi_client = None
        self.desktop_client = None

    def start_server(self):
        self.server.bind((self.host,self.port))
        self.server.listen()
        while self.running == True:
        	if self.connected<2:
           	 	client , addr = self.server.accept()
           	 	self.connected += 1 
    def video_thread():
    	#recv from pi
    	#send to desktop
   	def listen_for_movement():
   		while self.running == True:
   			command = self.desktop_client.recv(100).decode("ascii")
   			self.pi_client.send(command.encode("ascii"))
    def successful_event(self,client,dec_type):
    	if dec_type == "DESKTOP":
    		self.desktop_client == client
    		if self.pi_client != None:
    			thread = threading.Thread(target =self.video_thread)
    		else:
    			client.send("AWAITING_PI".encode("ascii"))
    	else:
    		self.pi_client = client
    		if self.desktop_client != None:
    			thread = threading.Thread(target =self.video_thread)
    		else:
    			client.send("AWAITING_DE".encode("ascii"))
   	def failed_event(client,message):
   		self.connected -= 1
   		client.send(message)
   		client.close()

    def check_declaration(self,client):
    	client.send("WHO_ARE_YOU".encode("ascii"))
    	declaration = client.recv(100).decode("ascii")
    	if declaration == "DESKTOP" && self.desktop_client == None :
    		self.successful_event(client,"DESKTOP")
    		self.listen_for_movement()
    	elif declaration == "DESKTOP" && self.desktop_client != None:
    		self.failed_event(client , "ALREADYDESKTOP")
    	elif declaration == "PI" && self.pi_client == None:
    		self.successful_event(client,"PI")
    		self.listen_for_movement()
    	elif declaration == "PI" && self.pi_client != None:
    		self.failed_event(client ,"ALREADYPI")
    	else:
    		print("Unknown Command!")

    			



		