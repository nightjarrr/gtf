# coding=UTF-8
import unittest
from getthefacts.fact import Fact, FactFormatter
from getthefacts.actor import Actor

class FactTests(unittest.TestCase):
    def testDefaultFactIsApplicableToAll(self):
        fact = Fact("%s is a word.")
        assert fact.isApplicableTo("Anything")

    def testGetFactAbout(self):
        fact = Fact("%s is a word.")
        factString = fact.getFactAbout(Actor("Book"))
        assert factString == "Book is a word."

class FactFormatterTests(unittest.TestCase):
    pass
