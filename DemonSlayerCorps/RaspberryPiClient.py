
from Encryption import EncryptionHandler
from GpioManager import GPIOManager
from videostreamer import VideoStreamer
import time
class RaspberryPiClient:
	def __init__(self):
		self.running = False
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.eh = EncryptionHandler()
		self.gpio = GPIOManager()
	def route_movement(self , message):
		pass

	def stream_video(self):
		pass

	def stop_threads_and_wait_for_desktop(self):
			self.running = False#stop  the video streaming thread!
			time.sleep(8)  #give enough time to close
			self.running = True
			self.wait_for_desktop()

	def listen_for_messages(self):
		while self.running == True:
			message = self.client.recv(100).decode("ascii")
			decrypted_message = eh.decrypted(message)
			if decrypted_message == '-DesktopDisconnect':
				thread = threading.Thread(target = self.stop_threads_and_wait_for_desktop)
				thread.start()
				break #stop listening for messages(end current thread)
			
			else:
				self.route_movement(decrypted_message)
	def start_threads(self):
		movement_thread = threading.Thread(target = self.listen_for_messages)
		streaming_thread = threading.Thread(target = self.stream_video)
		movement_thread.start()
		streaming_thread.start()

	def wait_for_desktop(self):
		server_response = self.client.recv(100).decode("ascii")
		if server_response == "SUCCESS":
			self.start_threads()
		else:
			self.client.close()
			print("issue!!")

	def check_response_and_proceed(self ,response):
			if response == "SUCCESS":
				print(colored("Successfully paired! Starting Client....","green"))
				self.start_threads()
			elif response == "AWAITING_DE":
				print(colored("Server says-> Waiting on desktop!" , "green"))
				self.wait_for_desktop()
			elif response == "ALREADYPI":
				print("Server says->"+
					colored("There is already a PI connected!", "red"))
			else:
				print("Server says->" ,
					colored("you have sent an unkown command!" , "red"))

	def start_client(self):
		self.running = True
		who_response = self.client.recv(100).decode("ascii")
		if who_response == "WHO_ARE_YOU":
			client.send("PI".encode("ascii"))
			server_response = self.client.recv(100).decode("ascii")
			self.check_response_and_proceed(server_response)