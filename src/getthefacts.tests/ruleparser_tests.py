# coding=UTF-8
from getthefacts.actor import Actor
from getthefacts.rules import *
import unittest

class NameRuleParserTests(unittest.TestCase):
    def testParse(self):
        name = "Winnie-The-Pooh"
        p = RuleParser("@" + name)
        rule = p.parse()
        assert rule == NameRule(name)

class NotRuleParserTests(unittest.TestCase):

    def testParse(self):
        name = "Winnie-The-Pooh"
        p = RuleParser("!@" + name)
        rule = p.parse()
        assert rule == NotRule(NameRule(name))

class TagRuleParserTests(unittest.TestCase):
    def testParse(self):
        p = RuleParser("bear")
        rule = p.parse()
        assert rule == TagRule("bear")

if __name__ == "__main__":
    unittest.main()
