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
        if self.facts is None or len(self.facts) == 0:
            return None

        fact = random.choice(self.facts).buildup()
        actors = self.actors
        if (len(fact.actorPlaceholders) > 0) \
            and (actors is None or len(actors) < len(fact.actorPlaceholders)):
            return None

        for placeholder in fact.actorPlaceholders:
            applicable = [actor for actor in actors if placeholder.rule.evaluate(actor)]
            if len(applicable) == 0:
                return None
            a = random.choice(applicable)
            placeholder.set_actor(a)
            actors.remove(a)
        if fact.ready():
            return fact.render()
        else:
            return None

class ActorBasedRandomFactChooser(FactChooser):
    def __init__(self, actor, facts, actors):
        self.actor = actor
        facts = [f for f in facts if f.isApplicableTo(actor)]        
        FactChooser.__init__(self, facts, actors)

    def choose(self):
        if self.facts is None or len(self.facts) == 0:
            return None

        fact = random.choice(self.facts).buildup()
        for placeholder in fact.actorPlaceholders:
            if placeholder.rule.evaluate(self.actor):
                placeholder.set_actor(self.actor)
                break

        actors = self.actors
        if (len(fact.actorPlaceholders) > 0) \
            and (actors is None or len(actors) < len(fact.actorPlaceholders)):
            return None

        for placeholder in fact.actorPlaceholders:
            if placeholder.has_actor():
                continue
            applicable = [actor for actor in actors if placeholder.rule.evaluate(actor)]
            if len(applicable) == 0:
                return None
            a = random.choice(applicable)
            placeholder.set_actor(a)
            actors.remove(a)
        if fact.ready():
            return fact.render()
        else:
            return None

