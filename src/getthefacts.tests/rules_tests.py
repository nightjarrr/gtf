# coding=UTF-8
import unittest
from getthefacts.actor import *
from getthefacts.rules import *

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

class AndRuleTests(unittest.TestCase):
    def testTrueAndFalseIsFalse(self):
        r = AndRule([TrueRule(), FalseRule()])
        assert not r.evaluate("some input")

    def testFalseAndTrueIsFalse(self):
        r = AndRule([TrueRule(), FalseRule()])
        assert not r.evaluate("some input")

    def testFalseAndFalseIsFalse(self):
        r = AndRule([FalseRule(), FalseRule()])
        assert not r.evaluate("some input")

    def testTrueAndTrueIsTrue(self):
        r = AndRule([TrueRule(), TrueRule()])
        assert r.evaluate("some input")

class OrRuleTests(unittest.TestCase):
    def testTrueOrFalseIsTrue(self):
        r = OrRule([TrueRule(), FalseRule()])
        assert r.evaluate("some input")

    def testFalseOrTrueIsTrue(self):
        r = OrRule([TrueRule(), FalseRule()])
        assert r.evaluate("some input")

    def testFalseOrFalseIsFalse(self):
        r = OrRule([FalseRule(), FalseRule()])
        assert not r.evaluate("some input")

    def testTrueOrTrueIsTrue(self):
        r = OrRule([TrueRule(), TrueRule()])
        assert r.evaluate("some input")

if __name__ == "__main__":
    unittest.main()
