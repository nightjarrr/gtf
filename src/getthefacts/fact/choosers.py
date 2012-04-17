# coding=UTF-8
import random
from . import *

# Seed the random generator when the module is imported.
random.seed();

class FactChooser:
    def __init__(self, facts, actors):
        self.facts = facts
        self.actors = actors

    def choose(self):
        pass

class RandomFactChooser(FactChooser):
    def __init__(self, facts, actors):
        FactChooser.__init__(self, facts, actors)

    def choose(self):
        fact = random.choice(self.facts).buildup()
        actors = self.actors
        for placeholder in fact.actorPlaceholders:
            applicable = [actor for actor in actors if placeholder.rule.evaluate(actor)]
            a = random.choice(applicable)
            placeholder.set_actor(a)
            actors.remove(a)
        if fact.ready():
            return fact.render()
        else:
            return None