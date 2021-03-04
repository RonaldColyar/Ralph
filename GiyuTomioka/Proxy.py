from Encryption import EncryptionHandler
import CLI
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
        self.logger = CLI.CommandLineInterface()

    def start_server(self):
        self.server.bind((self.host,self.port))
        self.server.listen()
        while self.running == True:
            if self.connected<2:
                client , addr = self.server.accept()
                self.connected += 1 
                self.check_declaration(client,addr)
    def video_thread():
        #recv from pi
        #send to desktop
        pass

    def listen_for_movement():
        while self.running == True:
            command = self.desktop_client.recv(100).decode("ascii")
            self.pi_client.send(command.encode("ascii"))

    def desktop_successful_event(self,client):
            self.desktop_client == client
            if self.pi_client != None:
                thread = threading.Thread(target =self.video_thread)
                thread.start()
                return True
            else:
                client.send("AWAITING_PI".encode("ascii"))
                return False
    def pi_successful_event(self,client):
            self.pi_client = client
            if self.desktop_client != None:
                thread = threading.Thread(target =self.video_thread)
                thread.start()
                return True
            else:
                client.send("AWAITING_DE".encode("ascii"))
                return False
        
    def failed_event(client,message,addr):

        self.connected -= 1
        client.send(message)
        client.close()

    #1.there can't be two desktops connected!
    #2.there can't be two pi connected!
    def check_declaration(self,client,addr):
        client.send("WHO_ARE_YOU".encode("ascii"))
        declaration = client.recv(100).decode("ascii")
        if declaration == "DESKTOP" and self.desktop_client == None : 
            if self.desktop_successful_event(client) == True:
                self.listen_for_movement()
        elif declaration == "DESKTOP" and self.desktop_client != None:
            self.failed_event(client , "ALREADYDESKTOP",addr)
        elif declaration == "PI" and self.pi_client == None:
            if self.pi_successful_event(client) == True:
                self.listen_for_movement()
        elif declaration == "PI" and self.pi_client != None:
            self.failed_event(client ,"ALREADYPI",addr)
        else:
            print("Unknown Command!")
            failed_event(client , "Unknown Command!",addr)

                




