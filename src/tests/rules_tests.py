import unittest
from rules import *

class TrueRuleTests(unittest.TestCase):
	def testAlwaysEvaluatesToTrue(self):
		r = TrueRule()
		assert r.evaluate(None)
		assert r.evaluate(5)
		assert r.evaluate("")
		assert r.evaluate(Actor("name"))
		assert r.evaluate([])

class FalseRuleTests(unittest.TestCase):
	def testAlwaysEvaluatesToFalse(self):
		r = FalseRule()
		assert not r.evaluate(None)
		assert not r.evaluate(5)
		assert not r.evaluate("")
		assert not r.evaluate(Actor("name"))
		assert not r.evaluate([])

class NotRuleTests(unittest.TestCase):
	def testNotTrueAlwaysEvaluatesToFalse(self):
		r = NotRule(TrueRule())
		assert not r.evaluate(None)
		assert not r.evaluate(5)
		assert not r.evaluate("")
		assert not r.evaluate(Actor("name"))
		assert not r.evaluate([])

class NameRuleTests(unittest.TestCase):
	def testEqualNamesEvaluatesToTrue(self):
		n = "some name"
		r = NameRule(n)
		assert r.evaluate(Actor(n))

	def testDifferentNamesEvaluatesToFalse(self):
		r = NameRule("name1")
		assert not r.evaluate(Actor("name2"))

class TagRuleTests(unittest.TestCase):
	def testEvaluatesToTrueIfTagged(self):
		r = TagRule("tag1")
		assert r.evaluate(Actor("name1", ["tag1"]))

	def testEvaluatesToFalseIfNotTagged(self):
		r = TagRule("tag1")
		assert not r.evaluate(Actor("name1", ["tag2"]))

if __name__ == "__main__":
    unittest.main()
