import unittest
import pyraspii 

class MainTest(unittest.TestCase):
	def test_comOUT(self):
		self.assertEqual(pyraspii.send_data(0, 0x44), None)

	def test_comIN(self):
		self.assertEqual(pyraspii.getData_from(0x44), 0)

if __name__ == '__main__':
	unittest.main()
