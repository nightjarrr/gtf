# coding=UTF-8
from getthefacts.actor import Actor
from getthefacts.rules import *
import unittest

class RuleParserTests(unittest.TestCase):
    def testParseNameRule(self):
        name = "Winnie-The-Pooh"
        p = RuleParser("@" + name)
        rule = p.parse()
        assert rule.__class__ is NameRule
        assert not rule.evaluate(Actor("Rabbit"))
        assert rule.evaluate(Actor(name))

    def testParseNameRuleRus(self):
        name = "Винни-Пух"
        p = RuleParser("@" + name)
        rule = p.parse()
        assert rule.__class__ is NameRule
        assert not rule.evaluate(Actor("Кролик"))
        assert rule.evaluate(Actor(name))

    def testParseNotRule(self):
        name = "Winnie-The-Pooh"
        p = RuleParser("!@" + name)
        rule = p.parse()
        assert rule.__class__ is NotRule
        assert rule.evaluate(Actor("Rabbit"))
        assert rule.evaluate(Actor("Piglet"))
        assert not rule.evaluate(Actor(name))

    def testParseTagRule(self):
        p = RuleParser("bear")
        rule = p.parse()
        assert rule.__class__ is TagRule
        assert not rule.evaluate(Actor("Piglet", ["small", "pig", "toy"]))
        assert rule.evaluate(Actor("Winnie-The-Pooh", ["bear", "toy"]))


if __name__ == "__main__":
    unittest.main()
