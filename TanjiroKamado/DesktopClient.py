import socket
import atexit
import commandhandler
from termcolor import colored
from colorama import init


class DesktopClient:
	init()# for colored text on windows
	def __init__(self):
		 self.running = True 
		 self.command_checker = commandhandler.CommandHandler()
		 self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		 try:
		 	self.client.connect(('127.0.0.1',50222))
		 except:
		 	self.running = False
		 	print(colored("Issue Connecting to Proxy Server!!" , "red"))

