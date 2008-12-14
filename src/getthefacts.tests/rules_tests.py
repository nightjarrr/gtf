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

    def testEquals(self):
        assert TrueRule() == TrueRule()
        assert not TrueRule() == FalseRule()

class FalseRuleTests(unittest.TestCase):
    def testAlwaysEvaluatesToFalse(self):
        r = FalseRule()
        assert not r.evaluate(None)
        assert not r.evaluate(5)
        assert not r.evaluate("")
        assert not r.evaluate(Actor("name"))
        assert not r.evaluate([])

    def testEquals(self):
        assert FalseRule() == FalseRule()
        assert not FalseRule() == TrueRule()

class NotRuleTests(unittest.TestCase):
    def testNotTrueAlwaysEvaluatesToFalse(self):
        r = NotRule(TrueRule())
        assert not r.evaluate(None)
        assert not r.evaluate(5)
        assert not r.evaluate("")
        assert not r.evaluate(Actor("name"))
        assert not r.evaluate([])

    def testEquals(self):
        assert NotRule(TrueRule()) == NotRule(TrueRule())
        assert not NotRule(TrueRule()) == FalseRule()
        assert not NotRule(TrueRule()) == NotRule(FalseRule())

class NameRuleTests(unittest.TestCase):
    def testEqualNamesEvaluatesToTrue(self):
        n = "some name"
        r = NameRule(n)
        assert r.evaluate(Actor(n))

    def testDifferentNamesEvaluatesToFalse(self):
        r = NameRule("name1")
        assert not r.evaluate(Actor("name2"))

    def testEquals(self):
        assert NameRule("name1") == NameRule("name1")
        assert NameRule("name1") != NameRule("name2")
        assert NameRule("name1") != TagRule("tag1")

class TagRuleTests(unittest.TestCase):
    def testEvaluatesToTrueIfTagged(self):
        r = TagRule("tag1")
        assert r.evaluate(Actor("name1", ["tag1"]))

    def testEvaluatesToFalseIfNotTagged(self):
        r = TagRule("tag1")
        assert not r.evaluate(Actor("name1", ["tag2"]))

    def testEquals(self):
        assert TagRule("tag1") == TagRule("tag1")
        assert TagRule("tag1") != TagRule("tag2")
        assert TagRule("tag1") != FalseRule()


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

    def testEquals(self):
        assert AndRule([TrueRule(), TrueRule()]) == AndRule([TrueRule(), TrueRule()])
        assert AndRule([TrueRule(), FalseRule()]) == AndRule([TrueRule(), FalseRule()])
        assert AndRule([TrueRule(), FalseRule()]) != AndRule([FalseRule(), TrueRule()])
        assert AndRule([TrueRule(), TrueRule()]) != AndRule([FalseRule(), FalseRule()])
        assert AndRule([TrueRule(), TrueRule()]) != OrRule([TrueRule(), TrueRule()])
        assert AndRule([TrueRule(), TrueRule()]) != TrueRule()

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

    def testEquals(self):
        assert OrRule([TrueRule(), TrueRule()]) == OrRule([TrueRule(), TrueRule()])
        assert OrRule([TrueRule(), FalseRule()]) == OrRule([TrueRule(), FalseRule()])
        assert OrRule([TrueRule(), FalseRule()]) != OrRule([FalseRule(), TrueRule()])
        assert OrRule([TrueRule(), TrueRule()]) != OrRule([FalseRule(), FalseRule()])
        assert OrRule([TrueRule(), TrueRule()]) != AndRule([TrueRule(), TrueRule()])
        assert OrRule([TrueRule(), TrueRule()]) != TrueRule()


if __name__ == "__main__":
    unittest.main()
