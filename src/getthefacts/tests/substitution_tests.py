# coding=UTF-8
import unittest
from getthefacts.fact import Substitution

class SubstitutionTests(unittest.TestCase):
    def testParse(self):
        s = Substitution("[big, beautiful]")
        assert s.choices == ["big", "beautiful"]

    def testResolve(self):
        s = Substitution("[big, beautiful]")
        r = s.resolve("%s is a [big, beautiful] tree.")
        assert r in ["%s is a beautiful tree.", "%s is a big tree."]


