# coding=UTF-8
import unittest
from getthefacts.actor import *

class ActorJsonFormatterTests(unittest.TestCase):
	def testRead(self):
		s = '{"name":"Name", "tags":["1","2"], "age":"24"}'
		a = ActorJsonFormatter().read(s)
		assert a.name == "Name"
		assert a.tags == ["1", "2"]
		assert a.age == "24"
