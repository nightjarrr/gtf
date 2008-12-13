"""
    Module name: rules.

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
        All objects, that are animal, bird or fish, but are nott big,
        satisfy this expression.


"""

class TrueRule:
    def evaluate(self, actor):
        return True
    
class FalseRule:
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

class RuleParser:
    def parseTag(self, str, pos):
        pass

    def parseName(self, str, pos):
        pass

    def parseNot(self, str, pos):
        pass

    def parseAnd(self, str, pos):
        pass

    def parseOr(self, str, pos):
        pass
    
    pass
