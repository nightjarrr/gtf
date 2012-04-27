# coding=UTF-8
from .. import rules

class FactFormatError(Exception): pass

class ActorPlaceholder():
    def __init__(self, index, rule):
        self.index = index
        self.rule = rule
        self.actor = None

    def set_actor(self, actor):
        self.actor = actor

    def has_actor(self):
        return self.actor is not None

class FactTemplate():
    """
    The abstract class that defines basic functionality of fact template.
    Fact template defines the format of fact pattern and how actor placeholders are specified
    """
    def __init__(self):
        self.__parsed__ = False

    def __parse__(self):
        """Parses the underlying template and returns a list of ActorPlaceholders defined in the template."""
        pass

    def buildup(self):
        """Returns an instance of Fact built from the template."""
        if not self.__parsed__:
            self.__actorPlaceholders__ = self.__parse__()
        return Fact(self, self.__actorPlaceholders__[:])

    def render(self, ctx):
        """Renders the underlying template using the provided dictionary {index:actor} filled from ActorPlaceholders"""
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

    def __init__(self, template, actorPlaceholders):
        self.template = template
        self.actorPlaceholders = actorPlaceholders

    def ready(self):
        return len(self.actorPlaceholders) == 0 or all([a.has_actor() for a in self.actorPlaceholders])

    def isApplicableTo(self, actor):
        """Return True if fact's rule evaluates to True on specifies actor."""
        return any([a.rule.evaluate(actor) for a in self.actorPlaceholders])

    def getFactAbout(self, actor):
        """Create concrete fact from fact pattern and specified actor."""
        self.actorPlaceholders[0].set_actor(actor)
        return self.render()

    def render(self):
        ctx = dict([(a.index, a.actor) for a in self.actorPlaceholders])
        return self.template.render(ctx)