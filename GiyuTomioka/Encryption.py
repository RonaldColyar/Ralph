import socket
from cryptography.fernet import Fernet
class EncryptionHandler:
	def make_key(self):
		key = Fernet.generate_key()
		with open("deata.key", "wb") as file:
			file.write(key)
