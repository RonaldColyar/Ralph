import socket
from cryptography.fernet import Fernet
class EncryptionHandler:
	def make_key(self):
		key = Fernet.generate_key()
		print(key)
		with open("deata.key", "wb") as file:
			file.write(key)
	def decrypted(self , message):
		with open("data.key", "rb") as file:
			key = file.read()
			f = Fernet(key)
			return f.decrypt(message)
 
EncryptionHandler().make_key()