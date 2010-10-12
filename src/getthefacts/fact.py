# coding=UTF-8
import random
import rules

# Seed the random generator when the module is imported.
random.seed();

class Substitution:
    """
    Substitution is a variable part of fact that consists of several possible
    choices which are injected in the resulted fact randomly.
    For example:
        %s is a [big, beautiful] tree.
        [big, beautiful] is a substitution, and a resulting fact may have 2 variants:
        %s is a big tree.
        %s is a beautiful tree.
    """
    def __init__(self, subst):
        self.subst = subst
        self.choices = [s.strip() for s in subst.strip().lstrip("[").rstrip("]").split(",")]

    def __choose__(self):
        return random.choice(self.choices)

    def resolve(self, fact):
        return fact.replace(self.subst, self.__choose__())

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

    def __init__(self, format, rule = rules.TrueRule()):
        """Initialize new instance of Fact."""
        self.format = format
        self.rule = rule

    def isApplicableTo(self, actor):
        """Return True if fact's rule evaluates to True on specifies actor."""
        return self.rule.evaluate(actor)

    def getFactAbout(self, actor):
        """Create concrete fact from fact pattern and specified actor."""
        return self.format % actor.name


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


class FactFormatter:

    """Read and write Facts to and from string."""

    def read(self, factString):
        """Read fact from string representation and return Fact instance."""
        if factString.find("|") == -1:
            return Fact(factString.strip())
        [format, ruleString] = factString.split("|", 1)
        rule = rules.RuleParser(ruleString).parse()
        return Fact(format, rule)

