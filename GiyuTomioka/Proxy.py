from Encryption import EncryptionHandler
import CLI
import socket
import threading 
from TimeoutManager import TimeTracker

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
        self.eh = EncryptionHandler()
        self.server.bind((self.host,self.port))
        self.server.listen()
        self.time_tracker = TimeTracker()
        

    def start_server(self):
        while self.running == True  and self.connected<2:
            client , addr = self.server.accept()
            self.connected += 1 
            thread = threading.Thread(target = self.check_declaration , args=(client,addr) )
            thread.start()
            

    def video_thread():
        #recv from pi
        #send to desktop
        pass

    def listen_for_movement():
        while self.running == True:
            command = self.desktop_client.recv(100).decode("ascii")
            if self.eh.decrypted(command) == "-DesktopDisconnect":
                self.desktop_client = None
            self.pi_client.send(command.encode("ascii"))

    #Checks if both clients are connected
    #when both are connected data will be streamed
    #between both client and desktop
    def successful_event(self,class_client_ref,client
                        ,other_client,message):

            class_client_ref = client
            if other_client != None: 
                client.send("SUCCESS".encode("ascii"))
                other_client.send("SUCCESS".encode("ascii"))
                thread = threading.Thread(target =self.video_thread)
                thread.start()
                self.listen_for_movement()
            else:
                client.send(message.encode("ascii"))
        
    def failed_event(client,message,addr):
        self.connected -= 1
        client.send(message)
        client.close()
        if message == "ALREADYPI":
            self.logger.conflicting_declaration("PI" , addr)
        else:
            self.logger.conflicting_declaration("Desktop" ,addr)
        self.logger.disconnection(addr)



    #1.there can't be two desktops connected!
    #2.there can't be two pi connected!
    def check_declaration_tier_three(self,declaration,client,addr):
        if declaration == "PI" and self.pi_client == None:
            self.successful_event(self.pi_client,
                    client,self.desktop_client,"AWAITING_DE") 
        elif declaration == "PI" and self.pi_client != None:
            self.failed_event(client ,"ALREADYPI",addr)
        elif declaration == None:
            return
        else:
            print("Unknown Command!")
            failed_event(client , "Unknown Command!",addr)


    def check_declaration_tier_two(self,declaration,addr,client):
        if declaration == "DESKTOP" and self.desktop_client == None :
                self.desktop_client == client 
                self.successful_event(self.desktop_client ,
                            client,self.pi_client,"AWAITING_PI") 
        elif declaration == "DESKTOP" and self.desktop_client != None:
                self.failed_event(client , "ALREADYDESKTOP",addr)

        else:
                self.check_declaration_tier_three(declaration,client,addr)


    def number_of_new_connector(self):
        if self.connected == 0 :
            return 1
        else:
            return 2
 

    def check_declaration(self,client,addr):

        connector_number = self.number_of_new_connector() #for clock purposes
        self.time_tracker.start_timer(client,connector_number) #prevent blocking!
        try:
            client.send("WHO_ARE_YOU".encode("ascii"))
            declaration = client.recv(100).decode("ascii")
            self.time_tracker.stop_timer(connector_number)
            self.check_declaration_tier_two(declaration,addr,client)
        except Exception as e:
            print("Issue")

      
                




