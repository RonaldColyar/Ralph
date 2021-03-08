import socket
import atexit
import time
import commandhandler
import threading
from Encryption import EncryptionHandler
from termcolor import colored
from colorama import init


class DesktopClient:
	init()# for colored text on windows
	def __init__(self):
		 self.running = False
		 self.command_checker = commandhandler.CommandHandler()
		 self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		 self.clock_running = False
		 self.beginning_time = time.time()
		 self.eh = EncryptionHandler()
		 try:
		 	self.client.connect(('127.0.0.1',50222))
		 except:
		 	self.running = False
		 	print(colored("Issue Connecting to Proxy Server!!" , "red"))

	def command_thread(self):
		while self.running == True:
			command = input(colored("Ralph Control Center " , "blue") +
							colored("Version 1.0 >" , "red")
				 )
			self.command_checker.check_command(command)


	def video_stream_thread(self):
		while self.running == True:
			pass
	def start_threads(self):
		#multi-line for readability
		video_thread = threading.Thread(target = self.video_stream_thread)
		command_thread = threading.Thread(target = self.command_thread)
		video_thread.start()
		command_thread.start()


	def monitor_time(self):
		while self.clock_running == True:
			current_time = time.time()
			elapsed_time = int(current_time - self.beginning_time)
			#one minute passes
			if elapsed_time >60:
				print("Timed Out!!")
				encrypted_message =self.eh.encrypted("-DesktopDisconnect")
				self.client.send(encrypted_message.encode("ascii"))
				self.client.close()
			else:
				print(f"{61 - elapsed_time} untill Timeout!")				

				
	def wait_on_pi(self):
		time_thread = threading.Thread(target = self.monitor_time)
		time_thread.start()
		# timeout functionality
		server_response = self.client.recv(100).decode("ascii")
		self.clock_running == False
		if server_response == "SUCCESS":
			self.start_threads()
		else:
			self.client.close()
			print("issue!!")
		

	def check_response_and_proceed(self ,response):
			if response == "SUCCESS":
				print(colored("Successfully paired! Starting Client....","green"))
				self.start_threads()
			elif response == "AWAITING_PI":
				print(colored("Server says-> Waiting on pi!" , "green"))
			elif response == "ALREADYDESKTOP":
				print("Server says->"+
					colored("There is already a desktop connected!", "red"))
			else:
				print("Server says->" ,
					colored("you have sent an unkown command!" , "red"))



	def start_client(self):
		self.running = True
		who_response = self.client.recv(100).decode("ascii")
		if who_response == "WHO_ARE_YOU":
			client.send("DESKTOP".encode("ascii"))
			server_response = self.client.recv(100).decode("ascii")
			self.check_response_and_proceed(server_response)