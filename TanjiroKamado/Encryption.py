import socket
from cryptography.fernet import Fernet
class EncryptionHandler:
	def __init__(self):
		with open("data.key" , "rb" ) as file:
			self.key = file.read()
			self.f= Fernet(self.key)
	def make_key(self):
		key = Fernet.generate_key()
		print(key)
		with open("deata.key", "wb") as file:
			file.write(key)
	def decrypted(self , message):
		with open("data.key", "rb") as file:
			return self.f.decrypt(message)
	def encrypted(message):
			return self.f.encrypt(message)
