
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