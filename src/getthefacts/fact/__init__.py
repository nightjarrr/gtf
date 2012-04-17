# coding=UTF-8
import random
from .. import rules

# Seed the random generator when the module is imported.
random.seed();

class FactFormatError(Exception): pass

class ActorPlaceholder():
    def __init__(self, index, rule):
        self.index = index
        self.rule = rule
        self.actor = None

    def set_actor(self, actor):
        self.actor = actor

class FactTemplate():
    """
    The abstract class that defines basic functionality of fact template.
    Fact template defines the format of fact pattern and how actor placeholders are specified
    """
    def parse(self):
        """Parses the underlying template and returns a list of ActorPlaceholders defined in the template."""
        pass

    def render(self, actors):
        """Renders the underlying template using the provided list of ActorPlaceholders
        with filled-in Actor instances."""
        pass

class Fact:

    """
    Defines the fact 'pattern' that can be applied to an actor.
    The 'Fact' can be regarded as a logical predicate that operates on the set
    of Actors.
    Predicate is a boolean function that is defined in an informal way, e.g. as
    a human-readable sentence.

    The 'Fact' consists of two parts, that together form a predicate: a pattern
    and a set of logical rules.
        *   The 'Pattern' is a human-readable representation of the 'Fact'.
            When a format string is substituted with the name of a concrete
            actor, a meaningful sentence is formed.

        *   Rules define a formal logical function that determines the result
            of a predicate for a concrete actor. Rules are defined in terms
            of actor's attributes, and impose restrictions on them.

            Example:

            The rule (["fish", "bird"],!big) defines all actors, that are fish
            or bird, and are not big.
    """

    def __init__(self, template):
        self.template = template
        self.actorPlaceholders = template.parse()

    def isApplicableTo(self, actor):
        """Return True if fact's rule evaluates to True on specifies actor."""
        return self.actorPlaceholders[0].rule.evaluate(actor)

    def getFactAbout(self, actor):
        """Create concrete fact from fact pattern and specified actor."""
        ap = self.actorPlaceholders[:]
        ap[0].set_actor(actor)
        return self.template.render(ap)

class FactChooser:

    """Choose random fact that is applicable to actor."""

    def __init__(self, facts):
        """Initialize new instance of FactChooser."""
        self.facts = facts
        # The dictionary where actors are mapped to the lists of facts
        # that are applicable to them.
        self.cache = {}

    def choose(self, actor):
        """Choose random fact that is applicable to actor."""
        applicableFacts = []
        if self.cache.has_key(actor.name):
            applicableFacts = self.cache[actor.name]
        else:
            # Filter facts: select only facts applicable to specified actor.
            applicableFacts = [fact for fact in self.facts
                               if fact.isApplicableTo(actor)]
            # Add filtered list to cache.
            self.cache[actor.name] = applicableFacts
            
        if len(applicableFacts) == 0:
            return None
        return random.choice(applicableFacts)
