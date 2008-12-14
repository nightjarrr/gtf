# coding=UTF-8
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

    def testParseWhitespace(self):
        name = "Winnie-The-Pooh"
        assert NotRule(NameRule(name)) == RuleParser("!   @" + name).parse()
        assert NotRule(NameRule(name)) == RuleParser("!\t@" + name).parse()
        assert NotRule(NameRule(name)) == RuleParser("! @" + name).parse()
        assert NotRule(NameRule(name)) == RuleParser("  !   @" + name).parse()
        assert NotRule(NameRule(name)) == RuleParser("!   @" + name + "    ").parse()
        assert NotRule(NameRule(name)) == RuleParser("!   @" + name + "\t  ").parse()

class TagRuleParserTests(unittest.TestCase):
    def testParse(self):
        p = RuleParser("bear")
        rule = p.parse()
        assert rule == TagRule("bear")

class AndRuleParserTests(unittest.TestCase):
    def testParse(self):
        p = RuleParser("(bear, !@Winnie-The-Pooh, !toy)")
        rule = p.parse()
        assert rule == AndRule([TagRule("bear"),
                                NotRule(NameRule("Winnie-The-Pooh")),
                                NotRule(TagRule("toy"))])

    def testParseEmbedded(self):
        p = RuleParser("((@Baloo, !big), bear, !@Winnie-The-Pooh, !toy)")
        rule = p.parse()
        assert rule == AndRule([AndRule([NameRule("Baloo"),
                                         NotRule(TagRule("big"))]),
                                TagRule("bear"),
                                NotRule(NameRule("Winnie-The-Pooh")),
                                NotRule(TagRule("toy"))])

    def testParseNegated(self):
        p = RuleParser("!(@Baloo, !big)")
        rule = p.parse()
        assert rule == NotRule(AndRule([NameRule("Baloo"), NotRule(TagRule("big"))]))

    def testParseWhitespace(self):
        # Sample rule: (@Baloo, bear, !toy)
        rule = AndRule([NameRule("Baloo"), TagRule("bear"), NotRule(TagRule("toy"))])
        assert rule == RuleParser("(@Baloo, bear, !toy)").parse()
        assert rule == RuleParser("\t(@Baloo, bear, !toy)").parse()
        assert rule == RuleParser(" (@Baloo, bear, !toy)").parse()
        assert rule == RuleParser("(\t@Baloo, bear, !toy)").parse()
        assert rule == RuleParser("( @Baloo, bear, !toy)").parse()
        assert rule == RuleParser("(  @Baloo, bear, !toy)").parse()
        assert rule == RuleParser("(@Baloo,bear,!toy)").parse()
        assert rule == RuleParser("(@Baloo,\tbear, !toy)").parse()
        assert rule == RuleParser("(@Baloo,     bear, !toy)").parse()
        assert rule == RuleParser("(@Baloo,bear,\t!toy)").parse()
        assert rule == RuleParser("(@Baloo,bear,!toy\t)").parse()
        assert rule == RuleParser("(@Baloo,bear,!toy    )").parse()
        assert rule == RuleParser("(@Baloo, bear, !toy)\t").parse()
        assert rule == RuleParser("(@Baloo, bear, !toy)    ").parse()

class OrRuleParserTests(unittest.TestCase):
    pass
    

if __name__ == "__main__":
    unittest.main()
