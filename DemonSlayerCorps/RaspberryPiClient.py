
from Encryption import EncryptionHandler


class RaspberryPiClient:
	def __init__(self):
		self.running = False
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.eh = EncryptionHandler()