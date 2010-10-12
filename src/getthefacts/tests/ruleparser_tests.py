# coding=UTF-8
from getthefacts.rules import *
import unittest

class NameRuleParserTests(unittest.TestCase):
    def testParse(self):
        name = "Winnie-The-Pooh"
        p = RuleParser("@" + name)
        rule = p.parse()
        assert rule == NameRule(name)

    def testParseWithSpaces(self):
        name = "Winnie The Pooh"
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

    def testParseWithSpaces(self):
        p = RuleParser("little bear")
        rule = p.parse()
        assert rule == TagRule("little bear")


class AndRuleParserTests(unittest.TestCase):
    
    def testParseSimple(self):
        assert AndRule([TagRule("tag1")]) == RuleParser("(tag1)").parse()

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

    def testParseWithSpaces(self):
        rule = AndRule([NameRule("Baloo the mighty"), TagRule("big bear"),
                        NotRule(TagRule("funny toy"))])
        assert rule == RuleParser("(@Baloo the mighty, big bear, !funny toy)").parse()

        
class OrRuleParserTests(unittest.TestCase):
    def testParseSimple(self):
        assert OrRule([TagRule("tag1")]) == RuleParser("[tag1]").parse()

    def testParse(self):
        p = RuleParser("[!bear, @Winnie-The-Pooh, toy]")
        rule = p.parse()
        assert rule == OrRule([NotRule(TagRule("bear")),
                               NameRule("Winnie-The-Pooh"),
                               TagRule("toy")])

    def testParseEmbeddedAnd(self):
        # Accept either Winnie-the-pooh, or big bear (not toy, and not named Baloo)
        p = RuleParser("[@Winnie-The-Pooh, (bear, big, !toy, !@Baloo)]")
        rule = p.parse()
        assert rule == OrRule([NameRule("Winnie-The-Pooh"),
                               AndRule([TagRule("bear"),
                                        TagRule("big"),
                                        NotRule(TagRule("toy")),
                                        NotRule(NameRule("Baloo"))])])

    def testParseEmbeddedOr(self):
        p = RuleParser("[@Winnie-The-Pooh, ([@Baloo, toy], big)]")
        rule = p.parse()
        assert rule == OrRule([NameRule("Winnie-The-Pooh"),
                               AndRule([OrRule([NameRule("Baloo"),
                                                TagRule("toy")]),
                                        TagRule("big")])])


class InvalidInputTests(unittest.TestCase):
    
    def testIfStartsWithInvalidSymbol(self):
        self.assertRaises(RuleParserError, RuleParser(",tag1").parse)
        self.assertRaises(RuleParserError, RuleParser(")tag1").parse)
        self.assertRaises(RuleParserError, RuleParser("]tag1").parse)

    def testFailIfEmptyTag(self):
        self.assertRaises(RuleParserError, RuleParser("").parse)

    def testFailIfReservedSymbolAtEol(self):
        self.assertRaises(RuleParserError, RuleParser("tag1,").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1(").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1)").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1[").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1]").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1!").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1@").parse)

    def testFailIfComplexRuleWithoutBraces(self):
        self.assertRaises(RuleParserError, RuleParser("tag1,tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("!tag1,tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("@tag1,tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1],tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1),tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1,(tag2)").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1,[tag2]").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1],[tag2]").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1),[tag2]").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1],(tag2)").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1),(tag2)").parse)


    def testFailIfAndBraceNotClosed(self):
        self.assertRaises(RuleParserError, RuleParser("(tag1").parse)
        self.assertRaises(RuleParserError, RuleParser("((tag1").parse)
        self.assertRaises(RuleParserError, RuleParser("((tag1)").parse)
        self.assertRaises(RuleParserError, RuleParser("([tag1]").parse)
        self.assertRaises(RuleParserError, RuleParser("[(tag1]").parse)

    def testFailIfOrBraceNotClosed(self):
        self.assertRaises(RuleParserError, RuleParser("[tag1").parse)
        self.assertRaises(RuleParserError, RuleParser("[[tag1").parse)
        self.assertRaises(RuleParserError, RuleParser("[[tag1]").parse)
        self.assertRaises(RuleParserError, RuleParser("[(tag1)").parse)
        self.assertRaises(RuleParserError, RuleParser("([tag1)").parse)

    def testFailIfNotMatchingBraces(self):
        self.assertRaises(RuleParserError, RuleParser("(tag1]").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1)").parse)

    def testFailIfEmptyBraces(self):
        self.assertRaises(RuleParserError, RuleParser("[]").parse)
        self.assertRaises(RuleParserError, RuleParser("()").parse)
        self.assertRaises(RuleParserError, RuleParser("(]").parse)
        self.assertRaises(RuleParserError, RuleParser("[)").parse)

    def testFailIfSingleCommaInsideBraces(self):
        self.assertRaises(RuleParserError, RuleParser("[,]").parse)
        self.assertRaises(RuleParserError, RuleParser("(,)").parse)

    def testFailIfNoSeparatorBetweenRules(self):
        self.assertRaises(RuleParserError, RuleParser("tag1[tag2]").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1(tag2)").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1!tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("tag1@name1").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1][tag2]").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1)[tag2]").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1](tag2)").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1)(tag2)").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1]tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1)tag2").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1]@name1").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1)!tag2").parse)

    def testFailIfEmptyNameRule(self):
        self.assertRaises(RuleParserError, RuleParser("@").parse)
        self.assertRaises(RuleParserError, RuleParser("!@").parse)
        self.assertRaises(RuleParserError, RuleParser("[@]").parse)
        self.assertRaises(RuleParserError, RuleParser("(@)").parse)

    def testFailIfEmptyNotRule(self):
        self.assertRaises(RuleParserError, RuleParser("!").parse)
        self.assertRaises(RuleParserError, RuleParser("[!]").parse)
        self.assertRaises(RuleParserError, RuleParser("(!)").parse)

    def testFailIfEmptyRuleInsideAndRule(self):
        self.assertRaises(RuleParserError, RuleParser("(@)").parse)
        self.assertRaises(RuleParserError, RuleParser("(,tag1)").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1,)").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1,,)").parse)
        self.assertRaises(RuleParserError, RuleParser("(tag1,,tag2)").parse)
        self.assertRaises(RuleParserError, RuleParser("(,,tag1)").parse)

    def testFailIfEmptyRuleInsideOrRule(self):
        self.assertRaises(RuleParserError, RuleParser("[@]").parse)
        self.assertRaises(RuleParserError, RuleParser("[,tag1]").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1,]").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1,,]").parse)
        self.assertRaises(RuleParserError, RuleParser("[tag1,,tag2]").parse)
        self.assertRaises(RuleParserError, RuleParser("[,,tag1]").parse)

if __name__ == "__main__":
    unittest.main()
