import unittest
import commandhandler



class CommandHandlerTests(unittest.TestCase):
	def test_valid_len(self):
		handler = commandhandler.CommandHandler("test")
		result = handler.command_is_valid_len("move 2")
		self.assertTrue(result)
		result = handler.command_is_valid_len("move 2 fwfds")
		self.assertFalse(result)
		
	def test_level_is_len(self):
		handler = commandhandler.CommandHandler("test")
		result = handler.command_is_valid_len("move 2")
		self.assertTrue(handler.level_is_int())
		handler2 = handler.command_is_valid_len("move t")
		self.assertFalse(handler.level_is_int())







unittest.main()
