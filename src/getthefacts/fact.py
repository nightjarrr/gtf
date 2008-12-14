# coding=UTF-8
from taggable import Taggable
import random


class Fact(Taggable):

    """
    Defines the fact 'pattern' that can be applied to an actor.
    The 'Fact' can be regarded as a logical predicate that operates on the set of Actors.
    Predicate is a boolean function that is defined in an informal way,
    e.g. as a human-readable sentence.

    The 'Fact' consists of two parts, that together form a predicate: a pattern and a set of logical rules.
        *   The 'Pattern' is a human-readable representation of the 'Fact'. When a format string is substituted with the
            name of a concrete actor, a meaningful sentence is formed.

        *   Rules define a formal logical function that determines the result of a predicate for a concrete actor.
            Rules are defined in terms of actor's attributes, and impose restrictions on them.

            Example:
            The rule (["fish", "bird"],!big) defines all actors, that are fish or bird, and are not big.
    """

    def __init__(self, format, tags = []):
        Taggable.__init__(self, tags)
        self.format = format

    def isApplicableTo(self, actor):
        return not self.hasTags() or self.isTaggedWithAny(actor.tags)

    def getFactAbout(self, actor):
        "Creates the concrete fact which is is built from the fact pattern and the specified actor"
        return self.format % actor.name

class FactChooser:
    "Lets choose a random fact for an actor that matches actor's tags"

    def __init__(self, facts):
        self.facts = facts
        # The dictionary where actors are mapped to the lists of facts
        # that are applicable to them.
        self.cache = {}
        random.seed();

    def choose(self, actor):
        applicableFacts = []
        if self.cache.has_key(actor.name):
            applicableFacts = self.cache[actor.name]
        else:
            # Filter the available facts and select only facts applicable to the specified actor.
            applicableFacts = [fact for fact in self.facts if fact.isApplicableTo(actor)]
            # Add the filtered list to cache, to avoid doing the same work in future.
            self.cache[actor.name] = applicableFacts
            
        if len(applicableFacts) == 0:
            return None
        return random.choice(applicableFacts)

class FactFormatter:
    "Enables saving and loading Facts to string"

    def read(self, factString):
        if factString.find("|") == -1:
            return Fact(factString.strip())
        [format, tagList] = factString.split("|", 1)
        tags = [tag.strip() for tag in tagList.split(",")]
        return Fact(format, tags)

    def write(self, fact):
        if fact.hasTags():
            return "%s| " % fact.format + ", ".join(fact.tags)
        else: return fact.format
