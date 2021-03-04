import unittest
import CLI
import Proxy
import socket
import threading
class CommandTesting(unittest.TestCase):
	def test_logger(self):
		logger = CLI.CommandLineInterface()
		logger.unknown_command("1232", "fff")
		logger.unknown_command("1232", "fff2")
		self.assertEqual(logger.log_number, 2)	
		logger.unknown_command("2312","31112")
		self.assertEqual(logger.log_number , 3)

class ProxyTesting(unittest.TestCase):
		
	def testproxy(self):
		desktop_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		pi_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		proxy = Proxy.Interface()
		proxy_thread = threading.Thread(target = proxy.start_server)
		proxy_thread.start()
		#connect
		desktop_client.connect(('127.0.0.1',50222))
		#gather the init message
		who_response = desktop_client.recv(100).decode("ascii")
		print(who_response)
		#should be who are you
		self.assertEqual(who_response , "WHO_ARE_YOU")
		#claim desktop
		desktop_client.send("DESKTOP".encode("ascii"))
		#recv response
		status_response = desktop_client.recv(100).decode("ascii")
		#should be waiting on raspberry pi 
		self.assertEqual(status_response , "AWAITING_PI")

	


if __name__ == '__main__':
	unittest.main()