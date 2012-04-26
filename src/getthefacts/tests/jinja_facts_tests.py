# coding=UTF-8
import unittest
from getthefacts.fact.jinja import ActorExtension
from getthefacts.actor import Actor
from getthefacts.rules import *
from jinja2 import Environment

class JinjaFactTemplateTests(unittest.TestCase):
    def testActorSyntax(self):
        e = Environment(extensions = [ActorExtension])
        template = e.from_string(' {% actor "author", "(old, beard)" %} ')
        assert e.actorPlaceholders is not None
        assert len(e.actorPlaceholders) == 1
        assert e.actorPlaceholders[0].index == 'author'
        assert e.actorPlaceholders[0].rule == AndRule([TagRule('old'), TagRule('beard')])

    def testActorWithoutRulesSyntax(self):
        e = Environment(extensions = [ActorExtension])
        template = e.from_string(' {% actor "author" %}')
        assert e.actorPlaceholders is not None
        assert len(e.actorPlaceholders) == 1
        assert e.actorPlaceholders[0].index == 'author'
        assert e.actorPlaceholders[0].rule == TrueRule()


