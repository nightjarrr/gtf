class Rule:
    def evaluate(self, actor):
        pass
    
class TrueRule(Rule):
    def evaluate(self, actor):
        return True
    
class FalseRule(Rule):
    def evaluate(self, actor):
        return False
    
class TagRule(Rule):
    def __init__(self, tag):
        self.tag = tag
        
    def evaluate(self, actor):
        return actor.isTaggedWith(self.tag)
    
class NameRule(Rule):
    def __init__(self, name):
        self.name = name
        
    def evaluate(self, actor):
        return self.name == actor.name
    
class NotRule(Rule):
    def __init__(self, baseRule):
        self.baseRule = baseRule
        
    def evaluate(self, actor):
        return not self.baseRule.evaluate(actor)
    
class CompositeRule(Rule):
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
    def __init__(self, source, pos = 0):
        self.ctx = RuleParserContext(source, pos)     

    def parse(self):
        pass

class RuleParserState:
    INITIAL = 0
    READING = 1
        
class RuleParserContext:
    
    def __init__(self, source, pos = 0):
        self.source = source    # The source string
        self.pos = pos          # The current position in the source
        self.hasErrors = False
        self.rule = None
        self.state = RuleParserState.INITIAL
    
    def readRule(self):
        ch = self.source[self.pos]
        if ch == "!":
            self.rule = NotRule(None)
        elif ch == "@":
            self.rule = NameRule(None)
        elif ch == "["
            self.rule = OrRule([])  
        elif ch == "("
            self.rule = AndRule([])
        elif ch.isalpha()
            self.rule = TagRule(None)  
    
    pass

class RuleFormatter:
    def read(self, rulesString):
        pass    