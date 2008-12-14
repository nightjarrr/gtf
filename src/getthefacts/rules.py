# coding=UTF-8
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


class RuleBase:

    """
    Base class for all rules.

    Overrides the __eq__ operator, but gives no implementation. This forces all
    decendants to override the equality operator to aviod errors.
    """

    def __eq__(self, other):
        return NotImplemented

class TrueRule:

    """
    This rule can be satisfied with any input object.
    It always returns "True" from the evaluate() method.
    """

    def evaluate(self, actor):
        return True

    def __eq__(self, other):
        return other.__class__ is TrueRule

    
class FalseRule:

    """
    This rule rejects any input object as non-satisfying.
    It always returns "False" from the evaluate() method.
    """

    def evaluate(self, actor):
        return False

    def __eq__(self, other):
        return other.__class__ is FalseRule


class TagRule:
    def __init__(self, tag):
        self.tag = tag
        
    def evaluate(self, actor):
        return actor.isTaggedWith(self.tag)

    def __eq__(self, other):
        return (other.__class__ is TagRule) and (self.tag == other.tag)


class NameRule:
    def __init__(self, name):
        self.name = name
        
    def evaluate(self, actor):
        return self.name == actor.name

    def __eq__(self, other):
        return (other.__class__ is NameRule) and (self.name == other.name)


class NotRule:
    def __init__(self, baseRule):
        self.baseRule = baseRule
        
    def evaluate(self, actor):
        return not self.baseRule.evaluate(actor)
    
    def __eq__(self, other):
        return (other.__class__ is NotRule) and \
               (self.baseRule == other.baseRule)


class CompositeRule:
    def __init__(self, baseRules):
        self.baseRules = baseRules

    def __eq__(self, other):
        return issubclass(other.__class__, CompositeRule) and \
               (self.baseRules == other.baseRules)


class AndRule(CompositeRule):
    def __init__(self, baseRules):
        CompositeRule.__init__(self, baseRules)
        
    def evaluate(self, actor):
        for rule in self.baseRules:
            if not rule.evaluate(actor): return False
        return True

    def __eq__(self, other):
        return other.__class__ is AndRule and \
               CompositeRule.__eq__(self, other)


class OrRule(CompositeRule):
    def __init__(self, baseRules):
        CompositeRule.__init__(self, baseRules)
        
    def evaluate(self, actor):
        for rule in self.baseRules:
            if rule.evaluate(actor): return True
        return False

    def __eq__(self, other):
        return other.__class__ is OrRule and \
               CompositeRule.__eq__(self, other)


class RuleParserError(Exception): pass


class RuleParserContext:

    """
    RuleParserContext stores information about the current stage of string
    parsing process.
    """

    def __init__(self, str, pos):
        """Initialize RuleParserContext with string and starting position."""
        self.str = str
        self.pos = pos
        self.hasErrors = False
        self.error = ""
        self.result = None
        self.isDone = False

    def getChar(self):
        """Return the character at the current position of the string."""
        return self.str[self.pos]

    def isEOL(self):
        """
        Return True if the current position is beyond the end of the line,
        and False otherwise.
        """
        return (self.pos >= len(self.str))

    def reportError(self, errorMsg):
        """Set the context state as erroneous and break the parsing process."""
        self.isDone = True
        self.hasErrors = True
        self.error = errorMsg

    def moveNext(self):
        """Move current context position to next character in string."""
        self.moveBy(1)

    def moveTo(self, newPos):
        """Move current context position to specified position."""
        self.pos = newPos

    def moveBy(self, delta):
        """Move current context position by specified delta."""
        self.pos += delta

class RuleParser:
    
    """
    RuleParser provides the ability to parse a string representation of rule
    into the rule object.
    """

    # List of recognized whitespace characters.
    WHITESPACES = [" ", "\t"]

    # List of reserves characters in this grammar.
    RESERVED = [",", "[", "]", "(", ")", "!", "@"]

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
        return self.__parseRule(ctx)

    def __parseRule(self, ctx):
        """
        Parse one rule using specified parsing context and return rule instance.
        """
        self.__skipWhitespace(ctx)

        if ctx.getChar() == "@":
            self.__parseName(ctx)
        elif ctx.getChar() == "!":
            self.__parseNot(ctx)
        elif ctx.getChar() == "[":
            self.__parseOr(ctx)
        elif ctx.getChar() == "(":
            self.__parseAnd(ctx)
        elif self.__isTextChar(ctx.getChar()):
            self.__parseTag(ctx)
        else:
            ctx.reportError("Invalid rule format: unknown rule at %d." %
                            ctx.pos)

        if ctx.hasErrors:
            raise RuleParserError, ctx.error
        else:
            return ctx.result

    def __isTextChar(self, ch):
        """Return True, if specified character is a text character."""
        return not ch in self.RESERVED

    def __parseText(self, ctx):
        """Parse the text value and return it as string."""
        start = ctx.pos
        while not ctx.isEOL() and self.__isTextChar(ctx.getChar()):
            ctx.moveNext()
        return ctx.str[start:ctx.pos].strip()

    def __parseTag(self, ctx):
        """Parse the TagRule from string."""
        ctx.result = TagRule(self.__parseText(ctx))

    def __parseName(self, ctx):
        """Parse the NameRule from string."""
        # Skip the "@" character.
        ctx.moveNext()
        ctx.result = NameRule(self.__parseText(ctx))

    def __parseNot(self, ctx):
        """Parse the NotRule from string."""
        # Skip the "!" character.
        ctx.moveNext()
        self.__skipWhitespace(ctx)
        # Wrap the rule next to "!" into the NotRule.
        ctx.result = NotRule(self.__parseRule(ctx))

    def __parseAnd(self, ctx):
        """Parse the AndRule from string."""
        # Skip the "(".
        ctx.moveNext()
        self.__skipWhitespace(ctx)
        rules = []
        while not ctx.isEOL() and (ctx.getChar() != ")"):
            r = self.__parseRule(ctx)
            rules.append(r)
            self.__skipWhitespace(ctx)
            # If the comma-separated list of rules isn't finished yet.
            if not ctx.isEOL() and ctx.getChar() == ",":
                # then move to the start of the next rule.
                ctx.moveNext()
                self.__skipWhitespace(ctx)

        if not ctx.isEOL() and (ctx.getChar() == ")"):
            ctx.moveNext()

        if len(rules) == 0:
            raise RuleParserError, "Incorrect or empty And rule definition. "

        ctx.result = AndRule(rules)

    def __parseOr(self, ctx):
        """Parse the OrRule from string."""
        # Skip the "[".
        ctx.moveNext()
        self.__skipWhitespace(ctx)
        rules = []
        while not ctx.isEOL() and (ctx.getChar() != "]"):
            r = self.__parseRule(ctx)
            rules.append(r)
            self.__skipWhitespace(ctx)
            # If the comma-separated list of rules isn't finished yet.
            if not ctx.isEOL() and ctx.getChar() == ",":
                # then move to the start of the next rule.
                ctx.moveNext()
                self.__skipWhitespace(ctx)

        if not ctx.isEOL() and (ctx.getChar() == ")"):
            ctx.moveNext()


        if len(rules) == 0:
            raise RuleParserError, "Incorrect or empty Or rule definition. "

        ctx.result = OrRule(rules)

    def __skipWhitespace(self, ctx):
        """
        Skip the whitespace from current position to the first non-whitespace
        symbol.
        """
        while not ctx.isEOL() and (ctx.getChar() in self.WHITESPACES):
            ctx.moveNext()