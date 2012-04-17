# coding=UTF-8
import random
from . import *
from .. import rules

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

class SimpleStringFactTemplate(FactTemplate):
    """
    Fact Template that defines current format of facts:
     - Single actor supported
     - Actor placeholder is '%s'
     - Substitutions supported
     - Single-line
     - Fact pattern separated from rule definition by '|'
     - Rule definition section is optional
     - Example of the format: "%s is a big tree.| (big, tree)"
    """

    def __init__(self, factString):
        FactTemplate.__init__(self)
        self.factString = factString

    def __parse__(self):
        rule = rules.TrueRule()
        format = self.factString
        if self.factString.find("|") > -1:
            [format, ruleString] = self.factString.split("|", 1)
            rule = rules.RuleParser(ruleString).parse()
        self.format = format
        self.__findSubstitutions__()
        hasActorplaceholder = self.factString.find("%s") > -1
        if hasActorplaceholder:
            return [ActorPlaceholder(0, rule)]
        else:
            return []

    def render(self, actors):
        fmt = self.__resolveSubstitutions__()
        return fmt % actors[0].name

    def __resolveSubstitutions__(self):
        f = self.format
        for s in self.substitutions:
            f = s.resolve(f)
        return f

    def __findSubstitutions__(self):
        self.substitutions = []
        s = self.format.split("[")
        if len(s) != len(self.format.split("]")):
            raise FactFormatError()
        for subst in s:
            if "]" in subst:
                subst = subst[0 : subst.find("]")]
                self.substitutions.append(Substitution("[" + subst + "]"))

class SimpleStringFactFormatter:

    """Read and write Facts to and from string."""

    def read(self, factString):
        t = SimpleStringFactTemplate(factString)
        return t.buildup()
