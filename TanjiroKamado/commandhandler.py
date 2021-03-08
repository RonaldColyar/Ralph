
import imagehandler
import threading
#SAMPLE COMMANDS

'''
#move 3
#move 2
#move 1
#record video
'''


class CommandHandler:
	def __init__(self , connection):
		self.connection = connection
		self.current_command = None
		#Movement levels
		self.level_one_message = "38"
		self.level_two_message = "320"
		self.level_three_message = "493"

		#validate the  structure 
	def command_is_valid_len(self, command): #-> bool
		separated_command = command.split(" ")
		if len(separated_command) == 2 :
			self.current_command = separated_command
			return True
		else:
			return False

	#check if level is int
	def level_is_int(self): #-> bool
		try:
			int(self.current_command[1])
			if int(self.current_command[1])<=3:
				return True
			else:
				return False
		except Exception as e:
			return False
	
		
	

	def check_command(self ,command):
		result = self.command_is_valid_len() #sets 'self.current_command'
		if self.current_command[0] == "move":
			if  result == True and self.level_is_int() == True:
				pass
			else:
				print("Issue With Command")
		elif self.current_command[0] == "record" and self.current_command[1] == "video":
			pass
		else:
			print("unknown command")




		