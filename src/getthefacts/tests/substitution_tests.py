# coding=UTF-8
import unittest
import re
from getthefacts.fact import Fact, FactFormatError
from getthefacts.fact.simple import Substitution, SimpleStringFactFormatter, SimpleStringFactTemplate
from getthefacts.actor import Actor

class SubstitutionTests(unittest.TestCase):
    def testParse(self):
        s = Substitution("[big, beautiful]")
        assert s.choices == ["big", "beautiful"]

    def testResolve(self):
        s = Substitution("[big, beautiful]")
        r = s.resolve("%s is a [big, beautiful] tree.")
        assert r in ["%s is a beautiful tree.", "%s is a big tree."]

class FactSubstitutionTests(unittest.TestCase):

    def testParse(self):
        f = SimpleStringFactFormatter().read("%s is a [big, beautiful] [tree, bird, fish].")
        s = f.template.substitutions
        assert len(s) == 2
        assert s[0].subst == "[big, beautiful]"
        assert s[1].subst == "[tree, bird, fish]"

    def testSingleSubstitution(self):
        f = SimpleStringFactFormatter().read("%s is a [big, beautiful] tree.")
        s = f.getFactAbout(Actor("Oak"))
        assert s in ["Oak is a beautiful tree.", "Oak is a big tree."]

    def testInvalidFormatRaisesError(self):
        f = SimpleStringFactTemplate("%s is a [big, beautiful tree.")
        self.assertRaises(FactFormatError, f.buildup)
