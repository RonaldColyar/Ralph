class CommandLineInterface:
	def __init__(self):
		self.log_number = 0
	def log_number_header(self):
		print(f"----Log Number {self.log_number}----")
		self.log_number += 1
	def log_footer(self):
		print("-----------------------------------------")
	def unknown_command(self,addr,message):
		self.log_number_header()
		print(f"client @({addr}) sent an unknown command")
		print(f"The unknown command was:{message}")
		self.log_footer()
	def conflicting_declaration(self,type_dec,addr):
		self.log_number_header()
		print(f"client @{addr} said they were {type_dec}")
		print(f"but there is already a declared {type_dec}")
		self.log_footer()
	def disconnection(self , addr):
		self.log_number_header()
		print(f"client @{addr} was successfully disconnected!")
		self.log_footer()
	def connection(self , addr , type_dec):
		self.log_number_header()
		print(f"client @ {addr} successfully connected as {type_dec}")
		self.log_footer()
	def successfully_paired(self):
		self.log_number_header()
		print("Successfully Connected to a desktop and pi!")
		print('Started communcation protocol!')
		self.log_footer()


