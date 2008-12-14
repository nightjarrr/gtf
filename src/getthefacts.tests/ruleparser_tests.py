# coding=UTF-8
from getthefacts.actor import Actor
from getthefacts.rules import *
import unittest

class NameRuleParserTests(unittest.TestCase):
    def testParse(self):
        name = "Winnie-The-Pooh"
        p = RuleParser("@" + name)
        rule = p.parse()
        assert rule.__class__ is NameRule
        assert rule.name == name

class NotRuleParserTests(unittest.TestCase):

    def testParse(self):
        name = "Winnie-The-Pooh"
        p = RuleParser("!@" + name)
        rule = p.parse()
        assert rule.__class__ is NotRule
        assert rule.baseRule.__class__ is NameRule
        assert rule.baseRule.name == name

class TagRuleParserTests(unittest.TestCase):
    def testParse(self):
        p = RuleParser("bear")
        rule = p.parse()
        assert rule.__class__ is TagRule
        assert rule.tag == "bear"

if __name__ == "__main__":
    unittest.main()
