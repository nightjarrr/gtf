# coding=UTF-8
import unittest
from getthefacts.fact import Fact, FactFormatter
from getthefacts.actor import Actor
from getthefacts.rules import AndRule, TagRule, TrueRule

class FactTests(unittest.TestCase):
    def testDefaultFactIsApplicableToAll(self):
        fact = Fact("%s is a word.")
        assert fact.isApplicableTo("Anything")

    def testGetFactAbout(self):
        fact = Fact("%s is a word.")
        factString = fact.getFactAbout(Actor("Book"))
        assert factString == "Book is a word."

class FactFormatterTests(unittest.TestCase):
    def testRead(self):
        f = FactFormatter()
        fact = f.read("%s is a big tree.| (big, tree)")
        assert fact.__class__ is Fact
        assert fact.format == "%s is a big tree."
        assert fact.rule == AndRule([TagRule("big"), TagRule("tree")])

    def testReadWithNoRules(self):
        f = FactFormatter()
        fact = f.read("%s is a word.")
        assert fact.rule == TrueRule()


