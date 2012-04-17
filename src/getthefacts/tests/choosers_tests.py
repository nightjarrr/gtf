# coding=UTF-8
import unittest
from getthefacts.fact.choosers import RandomFactChooser
from getthefacts.fact.simple import SimpleStringFactTemplate
from getthefacts.actor import Actor

class RandomFactChooserTests(unittest.TestCase):
	def testSingleFactIsChosen(self):
		template = SimpleStringFactTemplate("%s is out there.")
		actor = Actor("The truth")
		chooser = RandomFactChooser([template], [actor])
		c = chooser.choose()
		assert c is not None
		assert c == "The truth is out there."

	def testEmptyFactListRendersNone(self):
		actor = Actor("The truth")
		chooser = RandomFactChooser([], [actor])
		c = chooser.choose()
		assert c is None

	def testNoneFactListRendersNone(self):
		actor = Actor("The truth")
		chooser = RandomFactChooser(None, [actor])
		c = chooser.choose()
		assert c is None

	def testEmptyActorListRendersNone(self):
		template = SimpleStringFactTemplate("%s is out there.")
		chooser = RandomFactChooser([template], [])
		c = chooser.choose()
		assert c is None

	def testNoneActorListRendersNone(self):
		template = SimpleStringFactTemplate("%s is out there.")
		chooser = RandomFactChooser([template], None)
		c = chooser.choose()
		assert c is None

	def testNonFittingActorRendersNone(self):
		template = SimpleStringFactTemplate("%s is out there.|truth")
		actor = Actor("The truth")
		chooser = RandomFactChooser([template], [actor])
		c = chooser.choose()
		assert c is None
