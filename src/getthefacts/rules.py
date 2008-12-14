"""
    Module: rules.

    Description:

    This module contains classes that define the logical rules - a set of
    simple expressions that can be combined into complex expressions.

    Each instance of logical rule can take some object is input value,
    and produce a boolean result: whether the object satisfies the rule or not.

    The module also contains classes that can parse the rules from the string
    representation, and convert an existing rule to the equivalent string.

    Example string representation of complex rule:

    ([animal, bird, fish], !big)
    This string defines the following complex logical expression:
        All objects, that are animal, bird or fish,
        but are not big, satisfy this expression.

"""


class TrueRule:

    """
    This rule can be satisfied with any input object.
    It always returns "True" from the evaluate() method.
    """

    def evaluate(self, actor):
        return True

    
class FalseRule:

    """
    This rule rejects any input object as non-satisfying.
    It always returns "False" from the evaluate() method.
    """

    def evaluate(self, actor):
        return False


class TagRule:
    def __init__(self, tag):
        self.tag = tag
        
    def evaluate(self, actor):
        return actor.isTaggedWith(self.tag)


class NameRule:
    def __init__(self, name):
        self.name = name
        
    def evaluate(self, actor):
        return self.name == actor.name


class NotRule:
    def __init__(self, baseRule):
        self.baseRule = baseRule
        
    def evaluate(self, actor):
        return not self.baseRule.evaluate(actor)


class CompositeRule:
    def __init__(self, baseRules):
        self.baseRules = baseRules


class AndRule(CompositeRule):
    def __init__(self, baseRules):
        CompositeRule.__init__(self, baseRules)
        
    def evaluate(self, actor):
        for rule in self.baseRules:
            if not rule.evaluate(actor): return False
        return True


class OrRule(CompositeRule):
    def __init__(self, baseRules):
        CompositeRule.__init__(self, baseRules)
        
    def evaluate(self, actor):
        for rule in self.baseRules:
            if rule.evaluate(actor): return True
        return False


class RuleParserError(Exception): pass


class RuleParserContext: pass


class RuleParser:
    
    """
    RuleParser provides the ability to parse a string representation of rule
    into the rule object.
    """

    def __init__(self, ruleString):
        """Initialize RuleParser instance with string representation of rule."""
        self.str = ruleString

    def parse(self):
        """
        Parse the string into rule and return rule instance.

        If the string is not a correct representation of rule, a RuleParserError
        is raised.
        """
        ctx = RuleParserContext(self.str, 0)
        while not ctx.isDone:
            if ctx.currentChar == "@":
                self.__parseName(ctx)
            elif ctx.currentChar == "!":
                self.__parseNot(ctx)
            elif ctx.currentChar == "[":
                self.__parseOr(ctx)
            elif ctx.currentChar == "(":
                self.__parseAnd(ctx)
            elif ctx.currentChar.isalphanum():
                self.__parseTag(ctx)
            else:
                ctx.reportError("Invalid rule format: unknown rule at %d." %
                                ctx.currentPos)

        if ctx.hasErrors:
            raise RuleParserError, ctx.error
        else:
            return ctx.result

    def __parseTag(self, ctx):
        pass

    def __parseName(self, ctx):
        pass

    def __parseNot(self, ctx):
        pass

    def __parseAnd(self, ctx):
        pass

    def __parseOr(self, ctx):
        pass